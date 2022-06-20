"""Module where rules are defined"""

__author__ = "Heiner Alejandro Enis Caicedo"
__version__ = "0.0.1"

from abc import ABC, abstractmethod
from typing import Callable
from enum import Enum
import re

from faker import Faker

from cases.mapper import SimpleMapper

ex = Faker()

class RuleAbstract(ABC):
    """Abstract class for Rules"""
    @classmethod
    @abstractmethod
    def resolve(cls, **kwargs):
        """Build Rule Object. It gets the necessary parameters

        Returns:
            RuleAbstract: Rule Object
        """
        return cls(**kwargs)

class Ipv4PrivateRule(RuleAbstract):
    """Create a Private IPV4 if current value is not None"""
    def __init__(self, value):
        self._value = value

    def __call__(self):
        return ex.ipv4_private(address_class="a") if self._value else None 

    @classmethod
    def resolve(cls, **kwargs):
        value = kwargs["current_value"]
        return cls(value=value)

class DevicesNameFake(RuleAbstract):
    """Create a Devices name for devices"""
    def __call__(self):
        return ex.bothify(letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789', text="EMQU?????????????")

    @classmethod
    def resolve(cls, **kwargs):
        return cls()

class InheritanceRule(RuleAbstract):
    """Get values for other fields within tables or collection"""
    def __init__(self, row: dict, route: str, mapper: SimpleMapper, value: dict):
        self._row = row
        self._mapper = mapper
        self._route = route
        self._value = value

    def __call__(self):
        route_parts = self._route.split(".")

        if route_parts[0] == "self":
            return self._row[route_parts[1]]
        
        return self._mapper.get_value_for(self._value, self._route)

    @classmethod
    def resolve(cls, **kwargs):
        route = kwargs["route"]
        row = kwargs["row"]
        mapper = kwargs["mapper"]
        value = kwargs["current_value"]

        return cls(
            route=route,
            row=row,
            mapper=mapper,
            value=value
        )

    @classmethod
    def resolve(cls, **kwargs):
        route = kwargs["route"]
        row = kwargs["row"]
        mapper = kwargs["mapper"]
        value = kwargs["current_value"]
        template = kwargs["template"]

        return cls(
            route=route,
            row=row,
            mapper=mapper,
            value=value,
            template=template
        )

class StringRule(RuleAbstract):
    """Generate random string"""
    def __init__(self, value):
        self._value = value

    def __call__(self):
        if self._value:
            return ex.bothify(letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789', text="?????????????????")
        return None

    @classmethod
    def resolve(cls, **kwargs):
        value = kwargs["current_value"]
        return cls(value=value)


class RuleFactory:
    """Rule factory. Used to get the correct Rule class"""

    MAPPER = {
        "ipv4_private_random": Ipv4PrivateRule.resolve,
        "devices_name_fake": DevicesNameFake.resolve,
        "inheritance": InheritanceRule.resolve,
        "str_random": StringRule.resolve,
        "template": TemplateRule.resolve
    }

    @staticmethod
    def __get_filters(text: str):
        """Get filter in a Rule
            p.e:
                inheritance:database.table.field
        """
        parts = text.split(":")

        if len(parts) == 2:
            return parts
        return [text]

    @classmethod
    def get_rule(cls, rule_name: str) -> Callable:
        """Get correct Rule

        Args:
            rule_name (str): rule name

        Returns:
            Callable: Resolution function for values of Rule
        """
        rule_filters = cls.__get_filters(rule_name)

        if len(rule_filters) == 0:
            return cls.MAPPER[rule_filters[0]]
        
        return cls.MAPPER[rule_filters[0]]


        