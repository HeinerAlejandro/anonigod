from abc import ABC, abstractmethod
from typing import Any, List


class MapperAbsract(ABC):
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