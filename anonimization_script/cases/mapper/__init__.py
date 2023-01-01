"""Module to make a global data mapper"""

__author__ = "Heiner Alejandro Enis Caicedo"
__version__ = "0.0.1"

import shelve, tempfile, os

from pydash import flatten
from redis import Redis

from anonimization_script.utils import get_plain_rules, get_unique_name, get_connections
from anonimization_script.exceptions import MapNotFound
from anonimization_script.cases.mapper.abstracts import MapperAbsract


class MapperTypeStr(str):
    SIMPLE = "simple"
    REDIS = "redis"


def get_step_name(_index, step):
    
    if step == None:
        return _index
    elif step == "auto":
        return get_unique_name()
 
    return step


class SimpleMapper(MapperAbsract):
    """Simple mapper for anonimization
    
    It Saves maps between old value and new value into local disk using shelve
    python module. It help you to don't spend too much RAM saving value maps but
    accesing to them may be a little more slow.
    """
    def __init__(self, name, routes):
        
        self._name = name
        self._store = shelve.open(name)

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
        
    def __enter__(self):
        self._store = shelve.open(self._undo_fname)
        
    def __exit__(self):
        self._store.close()
        

        
    @classmethod
    def from_case_config(cls, data_config: dict):
        routes = flatten(routes)
        prefix_template = "{}.{}.step_{}"
        for case_name, case_config in data_config.items():
            for _index, step in enumerate(case_config["steps"]):
                prefix = prefix_template.format(
                    case_name, 
                    step["source_target"], 
                    get_step_name(_index, step.get("name", None))
                )
                case_routes = [f"{prefix}.{rule}" for rule in get_plain_rules(step["rules"])]
            routes.append(case_routes)
        return cls("mapper", routes)
    

class RedisMapper(MapperAbsract):
    """Mapper based on Redis
    
    It Saves maps between old value and new value as keys of a hash
    asociated to current route into Redis Database. Redis handles
    the RAM memory efficiently and helps you to access to the data fast.
    """
    def __init__(self, name, data_config: dict):
        self._name = name
        
        connection_data = get_connections(data_config)
        self._connection_data = Redis(**connection_data["conn"])

    def add_map(self, route: str, mappi: dict):
      self._connection.hset(route, mappi)

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
            return self._connection.hget(route, value)
        except KeyError:
            raise MapNotFound(f"Value '{value}' for route: {route} doesn't have mapped values")
    
    @classmethod
    def from_case_config(cls, data_config:dict):
        return cls("mapper", data_config)
    
    def __enter__(self):
        self._connection = Redis(self._connection_str)
        
    def __exit__(self):
        self._connection.close()
        
    
class MapperFactory:
    """Mapper Factory class to resolve specific mapper. Mapper availables by default are:
        - SimpleMapper
        - RedisMapper
    """
    MAPPER = {
        "simple": SimpleMapper,
        "redis": RedisMapper
    }
        
    @classmethod
    def get_mapper(cls, mapper_name: str):
        return cls.MAPPER.get(mapper_name, None)
    