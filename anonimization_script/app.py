
from asyncio import get_event_loop

import yaml

from anonimization_script.cases import Case
from anonimization_script.cases.meta import MetaCase
from anonimization_script.cases.mapper import MapperFactory


class App:
    def __init__(self, cases_file_dir: str):
        self.cases_file_dir = cases_file_dir
    
    def __enter__(self) -> None:
        raise NotImplemented("Context manager not implemented")
    
    def __exit__(self) -> None:
        raise NotImplemented("Context manager not implemented")
    
    def _get_mappers(self, data_config):
        mappers = {}
        mapper_adapters = MapperFactory.MAPPER
        cases_config = data_config["cases"]
        
        for adapter_type, adapter in mapper_adapters.items():
            mappers[adapter_type] = adapter.from_case_config(cases_config)
        
        return mappers
    
    def start(self):
        
        with open(self.cases_file_dir) as cases_file:
            
            data_config = yaml.safe_load(cases_file)
            
            connections = data_config["connections"]
            cases_anonigod = data_config["cases"]
            
            mappers = self._get_mappers(cases_anonigod, data_config)
    
            case_classes = [
                Case(
                    MetaCase.from_case_config(name, connections, cases_anonigod[name]),
                    mappers,
                    get_event_loop()
                ) for name in cases_anonigod
            ]

        for case in case_classes:
            case.start()
