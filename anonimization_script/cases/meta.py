"""Module to make meta config per step"""

__author__ = "Heiner Alejandro Enis Caicedo"
__version__ = "0.0.1"

import json
from abc import ABC, abstractmethod
from zlib import DEF_BUF_SIZE

from anonimization_script.exceptions import DBTypeNotValid
from anonimization_script.cases.db import DBAdapter, DBFactory


class Meta(ABC):
    """Abstract meta class"""
    @classmethod
    @abstractmethod
    def from_case_config(cls, case: str, connections: str, config: dict):
        pass
    
    @staticmethod
    @abstractmethod
    def __get_connections():
        pass
    
    @abstractmethod
    def get_db(self) -> DBAdapter:
        pass
    
    @abstractmethod
    def get_steps(self) -> list:
        pass
    
    @abstractmethod
    def get_case(self) -> str:
        pass
    
    @abstractmethod
    def get_config(self) -> dict:
        pass
    
class MetaCase(Meta):
    """Meta class for Case"""
    def __init__(self, case: str, db: DBAdapter, steps: list, config: dict):
        self._case = case
        self._db = db
        self._steps = steps
        self._config = config

    @staticmethod
    def __get_connections(connections: str, database_connections: dict) -> DBAdapter:
        """get connections from connection file

        Args:
            connections (str): connections available
            conn_name (str): DB connection name for cases
        Returns:
            DBAdapter: db object
        """
        with open(connections) as conn_file:
            connections_data = json.load(conn_file)
            
            db_item = connections_data.get(database_connections['connect_to'], None)
            
            if not db_item:
                raise DBTypeNotValid(f"Database connection with name: {database_connections['connect_to']} not found in connections file")
                
            db = DBFactory.get_db(
               db_item['dbtype']
            )(
                db_item['conn'], 
                db_item['dbtype'],
                database_connections["bulk_in"]
            )
            
        return db

    @classmethod
    def from_case_config(cls, case: str, connections: str, config: dict) -> Meta:
        """builder function for Meta object from step config

        Args:
            config (dict): Step config

        Returns:
            Meta: Meta object
        """
       
        db = cls.__get_connections(connections['connections_file'], {
                "connect_to": config["connection_name"],
                "bulk_in": config["bulk_in"]
            }
        )
        
        steps = config['steps']
    
        return cls(case=case, db=db, steps=steps, config=config)

    def get_db(self) -> DBAdapter:
        """Get db for its name

        Returns:
            DBAdapter: Database Adapter for connection
        """
        return self._db

    def get_steps(self) -> list:
        """Get rules

        Returns:
            list: Steps of case
        """
        return self._steps
    
    def get_case(self) -> str:
        return self._case
    
    def get_config(self) -> dict:
        return self._config