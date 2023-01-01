import click

from anonimization_script.exceptions import NoConnectionFileProvided
from anonimization_script.app import App

@click.group()
def cli():
    pass

@cli.command()
@click.option("--cases", "-c")
def start(cases: str) -> None:
    """Start the proccess anonigod

    Args:
        cases (str): file config of case

    Raises:
        NoConnectionFileProvided: Config file not provided
    """
    
    if cases == None:
        raise NoConnectionFileProvided("<cases>.yml must be provided")
    
    app = App(cases_file_dir=cases)
    app.start()
    
if __name__ == '__main__':
    start()