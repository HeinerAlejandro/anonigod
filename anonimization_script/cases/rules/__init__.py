"""Module where rules are defined"""

__author__ = "Heiner Alejandro Enis Caicedo"
__version__ = "0.0.1"

from abc import ABC, abstractmethod
from typing import Any, Callable
import re

from faker import Faker

from anonimization_script.exceptions import MapNotFound
from anonimization_script.cases.mapper.abstracts import MapperAbsract


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
    """Create a Private IPV4 if current value is not None
    
        Typical usage example:
            my_rule_obj = Ipv4PrivateRule(original_value)
            my_ipv4 = my_rule_obj()
    """
    def __init__(self, value):
        self._value = value

    def __call__(self):
        return ex.unique.ipv4_private(address_class="a") if self._value else None 

    @classmethod
    def resolve(cls, **kwargs):
        value = kwargs["current_value"]
        return cls(value=value)

class DevicesNameFake(RuleAbstract):
    """Create a Devices name for devices
        Typical usage example:
            my_rule_obj = DevicesNameFake()
            my_device_fake_name = my_rule_obj()
    """
    def __call__(self):
        return ex.unique.bothify(letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789', text="EMQU?????????????")

    @classmethod
    def resolve(cls, **kwargs):
        return cls()

class RegionFake(RuleAbstract):
    """Create a Region name
    
        Typical usage example:
            my_rule_obj = RegionFake()
            my_region_fake_name = my_rule_obj()
    """
    def __call__(self):
        return ex.unique.bothify(letters='123456789', text="REGION_?")

    @classmethod
    def resolve(cls, **kwargs):
        return cls()

class CityFake(RuleAbstract):
    """Create a City name
    
        Typical usage example:
            my_rule_obj = CityFake()
            my_city_fake_name = my_rule_obj()
    """
    def __call__(self):
        return ex.unique.city()

    @classmethod
    def resolve(cls, **kwargs):
        return cls()
        
class InheritanceRule(RuleAbstract):
    """Get values for other fields within tables or collection
        
        Typical usage example:
            my_rule_obj = InheritanceRule(
                row={"col_1": "English", "col_2": "Spanish", "col_3": "German"},
                route="case.database.table",
                mapper=mapper,
                value="old value to change"
            )
            
            my_inheriance_value = my_rule_obj()
            
        Attributes:
            row (dict): Dict for what you want to replace values
            mapper (Mapper): It's a mapper to replace dependence old values changed from previous case
            route (str): It's a route separate by dots of the data map (old_value: new_value) for dependences values
            value (Any): Value to be change
    """
    def __init__(self, row: dict, route: str, mapper: MapperAbsract, value: Any):
        self._row = row
        self._mapper = mapper
        self._route = route
        self._value = value

    def __call__(self):
        route_parts = self._route.split(".")

        if route_parts[0] == "self":
            return self._row[route_parts[1]]
        
        try:
            return self._mapper.get_value_for(self._value, self._route)
        except MapNotFound:
            return self._value

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

class TemplateRule(RuleAbstract):
    """Specify a template string to make data replaces
    
        Typical usage example:
            my_rule_obj = TemplateRule(
                row={"col_1": "English", "col_2": "Spanish", "col_3": "German"},
                mapper=mapper,
                value="old value to change",
                template="IN/[0-9a-zA-Z-]+/(?:ROUTER-)?{inheritance->([0-9a-zA-Z-_]+)->devices.devices.devices.host}"
            )
            
            my_replaced_data = my_rule_obj()
            
        Attributes:
            row (dict): Dict for what you want to replace values
            mapper (Mapper): It's a mapper to replace dependence old values changed from previous case
            value (Any): Value to be change
            template (str): Regex expresion that indicate how to change sections in data
    """
    
    def __init__(self, row: dict, mapper: MapperAbsract, value: Any, template: str):
        self._row = row
        self._mapper = mapper
        self._value = value
        self._template = template
        self._template_groups_regex = re.compile("{[^{}]+}+")

    def __call__(self):
        from anonimization_script.cases.rules.factories import RuleFactory
        
        new_value = self._value
        
        _variables = re.findall(self._template_groups_regex, self._template)
        
        _regexes = [var.strip("{}") for var in _variables]
        _regexes = [[reg.split("->")[0], reg.split("->")[1:]] for reg in _regexes]
        
        _template_regex = self._template
        
        for _regex in _regexes:
            pattern = self._template_groups_regex
            escaped = _regex[1][0]
            
            _template_regex = re.sub(pattern, escaped, _template_regex, count=1)
        
        match_expression = re.match(_template_regex, str(self._value))
        
        if not match_expression:
            return self._value
        
        groups = match_expression.groups()
        
        _data_for_resolve = {
            "row": self._row,
            "mapper": self._mapper,
            "current_value": None
        }
        
        for i, group in enumerate(groups):
            # TODO check this section, there's somthing weird

            if _regexes[i][0] == "fixed":
                continue
            
            _data_for_resolve["route"] = _regexes[i][1][1]
            
            _data_for_resolve["current_value"] = group
            
            _rule_class_resolver: RuleAbstract = RuleFactory.get_rule(_regexes[i][0])
            _rule = _rule_class_resolver(**_data_for_resolve)
            _result_from_rule = _rule()
            
            new_value = self._value.replace(group, _result_from_rule)

        return new_value

    @classmethod
    def resolve(cls, **kwargs):
        row = kwargs["row"]
        mapper = kwargs["mapper"]
        value = kwargs["current_value"]
        template = kwargs["template"]

        return cls(
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
            return ex.unique.bothify(letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789', text="?????????????????")
        return None

    @classmethod
    def resolve(cls, **kwargs):
        value = kwargs["current_value"]
        return cls(value=value)        