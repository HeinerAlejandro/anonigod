import importlib
from cases.db import DBAdapter, MYSQLAdapter
from cases.rules import RuleFactory
from anonimization_script.exceptions import BDTypeNotValid


def load_case(name):
    pass

def prepare_to_array(record):
    """Unify format of data from DBAdapter"""
    return record if type(record) not in [int, str, float, type(None)] else (record,)

def import_class(path: str, class_name: str):
    return importlib.import_module(path).__getattribute__(class_name)

def tranform_to_rules(factory: RuleFactory, rules):
    "Get Rule objecs from rule names"
    return { key: factory.get_rule(rule) for key, rule in rules.items() }

def get_plain_rules(rules):
    """Get Rules string routes for mapper"""
    keys = []
    
    for key in rules.keys():
        if type(rules[key]) != dict:
            keys.append(key)
        else:
            next_keys = get_plain_rules(rules[key])
            composed_keys = [".".join([key, next_key]) for next_key in next_keys]
            for composed_key in composed_keys:
                keys.append(composed_key)
    return keys
    
class DBFactory:

    DB_ADAPTERS = {
        "mysql": MYSQLAdapter
    }

    @classmethod
    def get_db(cls, dbtype: str) -> DBAdapter:
        """Get Adapter for DB Type

        Args:
            dbtype (str): dbtype

        Raises:
            BDTypeNotValid: DBType is not defined

        Returns:
            DBAdapter: DB Adapter
        """
        try:
            return cls.DB_ADAPTERS[dbtype]
        except KeyError:
            raise BDTypeNotValid(f"DB type '{dbtype}'is not a valid type, please use this instead {','.join(cls.DB_ADAPTERS.keys())}")
