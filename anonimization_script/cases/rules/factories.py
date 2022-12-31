from typing import Callable
import re

from anonimization_script.cases.rules.abstracts import RuleFactoryAbstract

from anonimization_script.cases.rules import (
    Ipv4PrivateRule,
    InheritanceRule,
    DevicesNameFake,
    TemplateRule,
    RegionFake,
    StringRule,
    CityFake
)


class RuleFactory(RuleFactoryAbstract):
    """Rule factory. Used to get the correct Rule class"""

    MAPPER = {
        "ipv4_private_random": Ipv4PrivateRule.resolve,
        "devices_name_fake": DevicesNameFake.resolve,
        "inheritance": InheritanceRule.resolve,
        "str_random": StringRule.resolve,
        "template": TemplateRule.resolve,
        "region_random": RegionFake.resolve,
        "city_random": CityFake.resolve
    }

    @staticmethod
    def __get_filters(text: str):
        """Get filter in a Rule
            p.e:
                inheritance:database.table.field
        """
        parts = re.split(":", text, maxsplit=1)

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
        
        return cls.MAPPER[rule_filters[0]]