"""Module to make meta config per step"""

__author__ = "Heiner Alejandro Enis Caicedo"
__version__ = "0.0.1"

import json
from abc import ABC, abstractmethod

from anonimization_script.utils import DBFactory, get_plain_rules
from anonimization_script.exceptions import BDTypeNotValid
from cases.db import DBAdapter

class Meta(ABC):
    """Abstract meta class"""
    @classmethod
    @abstractmethod
    def from_case_config(cls, config: dict):
        pass
    
class MetaCase(Meta):
    """Meta class for Case"""
    def __init__(self, case:str, dbs: dict[str, DBAdapter], rules: dict):
        self.case = case
        self._dbs = dbs
        self._rules = rules

    @staticmethod
    def __get_connections(connections: str):
        """get connections from connection file

        Args:
            connections (str): _description_

        Returns:
            _type_: _description_
        """
        with open(connections) as conn_file:
            connections_data = json.load(conn_file)
            
            conns = {
                item[0]: DBFactory.get_db(item[1]['dbtype'])(item[1]['conn'], item[1]['dbtype'])
                for item in connections_data.items()
            }
            
        return conns

    @classmethod
    def from_case_config(cls, case: str, config: dict) -> Meta:
        """builder function for Meta object from step config

        Args:
            config (dict): Step config

        Returns:
            Meta: Meta object
        """
       
        dbs = cls.__get_connections(config['connections'])
        
        rules = config['rules']
    
        return cls(case=case, dbs=dbs, rules=rules)

    def get_db_for(self, dbname: str) -> DBAdapter:
        """Get db for its name

        Args:
            dbname (str): connection name

        Raises:
            BDTypeNotValid: _description_

        Returns:
            DBAdapter: Database Adapter for connection
        """
        try:
            return self._dbs[dbname]
        except KeyError:
            raise BDTypeNotValid("DB Type must be within the registered database")

    def get_rules(self):
        """Get rules

        Returns:
            _type_: _description_
        """
        return self._rules