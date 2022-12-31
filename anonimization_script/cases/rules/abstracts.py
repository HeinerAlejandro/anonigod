from typing import Callable
from abc import ABCMeta, abstractmethod


class RuleFactoryAbstract(ABCMeta):
    
    @staticmethod
    @abstractmethod
    def __get_filters(text: str):
        pass 
    
    @classmethod
    @abstractmethod
    def get_rule(cls,  rule_name: str) -> Callable:
        pass