"""This module provide utils for use in cases"""

import importlib

from asyncio import gather, iscoroutine, AbstractEventLoop
import json
from typing import Any, Callable, List, Optional

from asgiref.sync import sync_to_async

from anonimization_script.cases.db import DBAdapter
from anonimization_script.cases.rules.abstracts import RuleFactoryAbstract

from faker import Faker


ex = Faker()


def get_connections(config: dict) -> dict:
    """Get Database connections"""
    connections = json.load(config["connections"])
    return connections


def get_unique_name():
    return ex.unique.bothify(letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789', text="?????????????")


def load_case(name: str):
    pass


def prepare_to_array(record: Any):
    """Unify format of data from DBAdapter"""
    return record if type(record) not in [int, str, float, type(None)] else (record,)


def import_class(path: str, class_name: str):
    """Util for import case module dynamically.
    It's usefull if you want to override the default Case class or you want extend
    from CaseAbstract class and create your own Case class

    Args:
        path (str): Module dir
        class_name (str): _description_

    Returns:
        Any: Case class
    """
    return importlib.import_module(path).__getattribute__(class_name)


def tranform_to_rules(factory: RuleFactory, rules):
    """Get Rule objecs from rule names"""
    return { key: factory.get_rule(rule) for key, rule in rules.items() }


def rule_for_deep_structure(level: str, item):
    """Generate plane keys for dict with more than two deeps"""

    value = item

    if "." in level:
        parts = level.split(".")
    else:
        parts = [level]

    
    for part in parts:
        value = value[part]

    return value


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


async def basic_separater(records: List):
    """Separater for records. Devide records into smaller fragments.

    Args:
        records (List): records
    """

    records_len = len(records)
    items_per_iter = 1000 if records_len > 1000 else 1
    
    if items_per_iter == 1:
        return [records]
        
    return [records[i:i + items_per_iter] for i in range(0, records_len)]


async def supress_indexs(adapter: DBAdapter, main_func: Callable, **kwargs):
    result = adapter.delete_all_index(kwargs["target"])
    await main_func()
    adapter.create_all_index(result)


def get_evelop_update_func(dbtype: str):
    if dbtype == "mysql":
        return supress_indexs
    return None


async def do_bash_operation(
    loop: AbstractEventLoop,
    records: List, 
    operation: Callable, 
    args_update: dict, 
    args_envelope: dict,
    adapter: DBAdapter,
    step_func: Optional[Callable]=basic_separater,
    envelop: Optional[Callable]=None):
    
    async def logic_func():
        bashes = await step_func(records)
        tasks = []

        if iscoroutine(operation):
            for bash in bashes:
                task = loop.create_task(operation(bash, args_update))
                tasks.append(task)
        else:
            for bash in bashes:
                async_operation = sync_to_async(operation)
                task = loop.create_task(async_operation(bash, args_update))
                tasks.append(task)

        await gather(*tasks)
    await envelop(adapter, logic_func, **args_envelope) if envelop else logic_func()