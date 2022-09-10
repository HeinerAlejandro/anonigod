"""Module to make a global data mapper"""

__author__ = "Heiner Alejandro Enis Caicedo"
__version__ = "0.0.1"

import shelve
from abc import ABC, abstractmethod
from typing import Any, List

from anonimization_script.exceptions import MapNotFound

class Mapper(ABC):
    """Mapper abstract class"""
    @abstractmethod
    def add_map(self, route: str, mappi: dict):
        """Add values map to the shelve db

        Args:
            route (str): path to save the map
            mappi (dict): mappi to be saved
        """
        pass

    @abstractmethod
    def get_value_for(self, value: Any, route: str):
        """Get some value from the maps

        Args:
            value (Any): original value to get fake value
            route (str): map value path
        """
        pass
    
    @classmethod
    @abstractmethod
    def from_case_config(cls, name: str, routes: List[str]):
        """Construct mapper from the config

        Args:
            name (str): shelve db name
            routes (List[str]): routes where maps get save
        """
        pass


class SimpleMapper(Mapper):
    """Simple mapper for anonimization"""
    def __init__(self, name, routes):
        
        self._store = shelve.open(f"{name}")

        for route in routes: 
            self._store[route] = {}

    def add_map(self, route: str, mappi: dict):
        maps = self._store[route]
        maps.update(mappi)
        self._store[route] = maps

    def get_value_for(self, value, route: str):
        """get mapped value

        Args:
            value (any): value stored in mapper
            route (str): value route in mapper

        Raises:
            MapNotFound: Data not foound in mapper

        Returns:
            Any: Value from mapper
        """
        try:
            return self._store[route][value]
        except KeyError:
            raise MapNotFound(f"Value '{value}' for route: {route} doesn't have mapped values")
    
    @classmethod
    def from_case_config(cls, name: str, routes: List[str]):
        return cls(name, routes)

