# Extractor Scripts

Anonimization Scripts abstraction classes.

## Development installation

    $ git clone [aca va el repositorio]
    $ cd anonimization_script
    $ pipenv install
    $ pipenv install --dev
    $ pipenv run pre-commit install --install-hooks

## Run tests

    $ cd tests
    $ coverage run -m unittest discover

This will ignore the `runner.py` script and run the tests in the `test_*` files in test directory. The output for this
command is minimum.

If a similar runner.py output is desired use:

    $ coverage run -m unittest discover -v


### Show coverage tests

#### Text

    $ coverage report

#### HTML

    $ coverage html

This will create a `htmlcov` directory on run directory look with the browser.

## Build package
To build the installable packages you can choose.

First sync setup.py from Pipfile with these commands:

    $ pipenv run pipenv-setup sync
    $ pipenv run pipenv-setup sync --dev

### Wheel file

    $ pipenv run python setup.py bdist_wheel

### Debian package

    $ pipenv run python setup.py --command-packages=stdeb.command bdist_deb

## Generate development documentation

    cd docs
    sphinx-apidoc -Pfe -o source ../anonimization_script
    make html

Do `make help` for options format options.

## TODO
 - [x] Do the *Development install* doc.
 - [x] Do the *Generate development documentation* doc.
