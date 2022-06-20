import click
import yaml

from anonimization_script.exceptions import NoConnectionFileProvided
from anonimization_script.utils import import_class, get_plain_rules
from cases.meta import MetaCase
from cases.mapper import SimpleMapper

@click.group()
def cli():
    pass

@cli.command()
@click.option("--cases", "-c")
def start(cases: str):
    if cases == None:
        raise NoConnectionFileProvided("<cases>.yml must be provided")

    with open(cases) as cases_conf:
        cases_anonigod = yaml.safe_load(cases_conf)
    
        case_classes = [
            import_class(
                cases_anonigod[name]["path"], 
                cases_anonigod[name]["class"]
            )(
                MetaCase.from_case_config(cases_anonigod[name]),
                SimpleMapper.from_case_config(name, get_plain_rules(cases_anonigod[name]["rules"]))
            ) for name in cases_anonigod
        ]

    for case in case_classes:
        case.start()

if __name__ == '__main__':
    start()