"""Module to make a case class from config"""

__author__ = "Heiner Alejandro Enis Caicedo"
__version__ = "0.0.1"

import re
from asyncio import AbstractEventLoop
from abc import ABC, abstractmethod
from typing import Any, List

import pandas as pd
import numpy as np

from anonimization_script.cases.meta import Meta
from anonimization_script.cases.mapper.abstracts import MapperAbsract
from anonimization_script.cases.mapper import MapperFactory, MapperTypeStr

from anonimization_script.cases.rules.factories import RuleFactory
from anonimization_script.utils import (
    tranform_to_rules, 
    get_plain_rules, 
    rule_for_deep_structure, 
    do_bash_operation,
    get_evelop_update_func
)

from anonimization_script.exceptions import MapperNotFound


class AbstractCase(ABC):
    
    @abstractmethod
    def _get_table_rules(self, rule_levels: list, table_rule: dict):
        """Get rules from table config

        Args:
            rule_levels (list): anidation levels
            table_rule (dict): table rules
        """
        pass
    
    @abstractmethod
    def _set_context_for_rule(self, rule_parts: list):
        """Set specific context value depeding on rule_type 

        Args:
            rule_parts (list): list with rule type and rule value
        """
        pass
    
    @abstractmethod
    def _get_format_to_save(self, step: str, table: str, key: str):
        """Get formated route value for Mapper's route

        Args:
            step (str): process step 
            table (str): current table in the process
            key (str): column or field to modify
        """
        pass
    
    @abstractmethod
    def _get_mapi_structure(self, value: Any):
        """Get map value structure for mapper

        Args:
            value (Any): Value to put in correct format
        """
        pass
    
    @abstractmethod
    def _get_specific_mapper(self, mapper_target: str) -> MapperAbsract:
        pass
    
    @abstractmethod
    def _get_mapper_from_config(self):
        pass
    
    @abstractmethod
    def _save_mapi(self, route: str, value: Any):
        """Save map value in case mapper

        Args:
            route (str): route key to save value in mapper
            value (Any): value to save in mapper
        """
        pass
    
    @abstractmethod
    def _set_mapper_from_config():
        """This method is used to set mapper to the class context to have
        a unique mapper for step
        """
        pass
    
    @abstractmethod
    def _apply_rules(self, df: pd.DataFrame, rules: dict) -> pd.DataFrame:
        """Apply rules to data

        Args:
            df (pd.DataFrame): Representative Data Structure
            rules (dict): map between rule names and function to apply it
            
        Returns:
            df (DataFrame): Data with rules applied
        """
        pass
    
    @abstractmethod
    def start(self):
        """Start Case for Data anonimization"""
        pass
    
    
class Case(AbstractCase):

    TRIGGERS = {
        "inheritance": lambda self, value: self._context.update({"route": value}),
        "template": lambda self, value: self._context.update({"template": value}) 
    }
    # TODO: adjust code to mappers array
    def __init__(self, meta: Meta, mappers: List[MapperAbsract], loop: AbstractEventLoop):
        self._meta = meta
        self._mappers = mappers
        self._loop = loop
        self._context = {
            "mapper": None
        }
        self.current_step = None
        self.step_index = None
        
    def _get_table_rules(self, rule_levels: list, table_rule: dict):
        rules = {}
        for level in rule_levels:
            rules[level] = rule_for_deep_structure(level, table_rule)
        return rules
    
    def _set_context_for_rule(self, rule_parts: list):
        rule_type = rule_parts[0]
        operation = self.__class__.TRIGGERS[rule_type]
        
        rule_value = rule_parts[1]
        operation(self, rule_value)
    
    def _get_format_to_save(self, key: str):
        config = self._meta.get_config()
        database_target = config["database_target"]
        source_target = self._current_step["source_target"]
        
        return f"{self._meta.get_case()}.{database_target}.{self.step_index}.{source_target}.{key}"
    
    def _get_mapi_structure(self, value: Any):
        return { self._context["current_value"]: value }
    
    def _save_mapi(self, route: str, value: Any, mapper_type: str):
        mapper = self._get_specific_mapper(mapper_type)
        mapi = self._get_mapi_structure(value) 
        mapper.add_map(route, mapi)
    
    def _get_specific_mapper(self, mapper_target: str) -> MapperAbsract:
        
        mapper_class = MapperFactory.get_mapper(mapper_target)
        
        mappers = [mapper for mapper in self._mappers if isinstance(mapper, mapper_class)]
        
        if not mappers:
            raise MapperNotFound(f"Mapper type {mapper_target} was not found. \
            Mapper types vailables are: {list(MapperTypeStr)}")
        
        return mappers[0]
    
    def _set_mapper_from_config(self):
        
        mapper_target = self.current_step.get("mapper_database_target", None)
        
        if not mapper_target:
            config = self._meta.get_config()
            mapper_target = config.get("mapper_database_target", None)
            
            if not mapper_target:
                raise MapperNotFound("Your are not specify some mapper within case.yml config file")

        self._context["mapper"] = self._get_specific_mapper(mapper_target) 
            
    # TODO: Agregar tipado generico para df
    def _apply_rules(self, df: pd.DataFrame, rules: dict) -> pd.DataFrame:
        
        NONE_VALUES = (None, "null", np.nan, "")
        
        len_df = len(df)
        rules_functions = tranform_to_rules(RuleFactory, rules)
        
        self._set_mapper_from_config()
        
        for i in range(len_df): 
            row = df.loc[i]
            for key in rules_functions.keys():
                self._context["current_value"] = row[key]
                rule_parts = re.split(":", rules[key], maxsplit=1)
                
                if len(rule_parts) == 2:
                    self._set_context_for_rule(rule_parts)

                if not self._context["current_value"] in NONE_VALUES:
                    self._context["row"] = row.to_dict()
                    # Execute rule
                    row[key] = rules_functions[key](**self._context)()
                            
                    df.loc[i] = row
                            
                    row_to_save = self._get_format_to_save(key)
                    
                    self._save_mappi(row_to_save, row[key])

                    row_dict = row.to_dict()
                    self._context["row"] = row_dict
                    
        return df
       
    def start(self) -> None:
        
        steps = self._meta.get_steps()
        
        adapter = self._meta.get_db()
        adapter.copy_database(
            self._meta.get_config()["database_target"],
            list(set([step["source_target"] for step in steps]))
        )
        
        for step_index, step in enumerate(steps):
            self.current_step = step
            self.step_index = step_index
        
            table_target = step["source_target"]
            rules_for_step = step["rules"]

            # TODO: Este clone esta raro para el caso de steps, revisar
            
            rule_levels = get_plain_rules(rules_for_step)
            
            table_rules = self._get_table_rules(rule_levels, rules_for_step)
            
            columns = [column for column in rules_for_step]
            # TODO: Adjust to batch processing
            df_fake = adapter.get_all(columns=columns, target=table_target)
            df_fake = self._apply_rules(df_fake, table_rules)
            adapter.update_target(df_fake, table_target)