
from asyncio import get_event_loop

import yaml
from pydash import flatten

from anonimization_script.cases import Case
from anonimization_script.utils import get_plain_rules
from anonimization_script.cases.meta import MetaCase
from anonimization_script.cases.mapper import SimpleMapper

class App:
    def __init__(self, cases_file: str):
        self.cases_file = cases_file
    
    def __enter__(self) -> None:
        raise NotImplemented("Context manager not implemented")
    
    def __exit__(self) -> None:
        raise NotImplemented("Context manager not implemented")
    
    def start(self):
        routes = []
        
        with open(self.cases_file) as cases_file:
            cases_anonigod = yaml.safe_load(cases_file)

            for name in cases_anonigod:
                case_routes = [f"{name}.{rule}" for rule in get_plain_rules(cases_anonigod[name]["rules"])]
                routes.append(case_routes)

            routes = flatten(routes)
            simple_mapper =  SimpleMapper.from_case_config("mapper", routes)

            case_classes = [
                Case(
                    MetaCase.from_case_config(name, cases_anonigod[name]),
                    simple_mapper,
                    get_event_loop()
                ) for name in cases_anonigod
            ]

        for case in case_classes:
            case.start()
