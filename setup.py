"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
Modified by Madoshakalaka@Github (dependency links added)
"""

# Always prefer setuptools over distutils
from os import path
from setuptools import setup, find_packages


# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    # This is the name of your project. The first time you publish this
    # package, this name will be registered for you. It will determine how
    # users can install this project, e.g.:
    #
    # $ pip install sampleproject
    #
    # And where it will live on PyPI: https://pypi.org/project/sampleproject/
    #
    # There are some restrictions on what makes a valid project name
    # specification here:
    # https://packaging.python.org/specifications/core-metadata/#name
    name="anonimization_script",  # Required
    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    #
    # For a discussion on single-sourcing the version across setup.py and the
    # project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version="0.0.1",  # Required
    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#summary
    description="Abstracción de un script de extracción.",  # Optional
    # This is an optional longer description of your project that represents
    # the body of text which users will see when they visit PyPI.
    #
    # Often, this is the same as your README, so you can just read it in from
    # that file directly (as we have already done above)
    #
    # This field corresponds to the "Description" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=long_description,  # Optional
    # Denotes that our long_description is in Markdown; valid values are
    # text/plain, text/x-rst, and text/markdown
    #
    # Optional if long_description is written in reStructuredText (rst) but
    # required for plain-text or Markdown; if unspecified, "applications should
    # attempt to render [the long_description] as text/x-rst; charset=UTF-8 and
    # fall back to text/plain if it is not valid rst" (see link below)
    #
    # This field corresponds to the "Description-Content-Type" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    # This should be a valid link to your project's main homepage.
    #
    # This field corresponds to the "Home-Page" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    # url="https://github.com/pypa/sampleproject",  # Optional
    # This should be your name or the name of the organization which owns the
    # project.
    author="Heiner Enis",  # Optional
    # This should be a valid email address corresponding to the author listed
    # above.
    author_email="heiner.enis@emqu.net",  # Optional
    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    # classifiers=[  # Optional
    #     # How mature is this project? Common values are
    #     #   3 - Alpha
    #     #   4 - Beta
    #     #   5 - Production/Stable
    #     "Development Status :: 3 - Alpha",
    #     # Indicate who your project is intended for
    #     "Intended Audience :: Developers",
    #     "Topic :: Software Development :: Build Tools",
    #     # Pick your license as you wish
    #     "License :: OSI Approved :: MIT License",
    #     # Specify the Python versions you support here. In particular, ensure
    #     # that you indicate whether you support Python 2, Python 3 or both.
    #     # These classifiers are *not* checked by 'pip install'. See instead
    #     # 'python_requires' below.
    #     "Programming Language :: Python :: 2",
    #     "Programming Language :: Python :: 2.7",
    #     "Programming Language :: Python :: 3",
    #     "Programming Language :: Python :: 3.5",
    #     "Programming Language :: Python :: 3.6",
    #     "Programming Language :: Python :: 3.7",
    # ],
    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    # keywords="sample setuptools development",  # Optional
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(),  # Required
    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. If you
    # do not support Python 2, you can simplify this to '>=3.5' or similar, see
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4",
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=["Click", "attrs==21.4.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", 'cached-property==1.5.2', "cerberus==1.3.4; python_version >= '2.7'", "certifi==2022.5.18.1; python_version >= '3.6'", "chardet==4.0.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", "charset-normalizer==2.0.12; python_version >= '3.5'", "colorama==0.4.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", "dataclasses-json==0.5.7; python_version >= '3.6'", 'distlib==0.3.4', "idna==3.3; python_version >= '3.5'", 'iniconfig==1.1.1', "marshmallow==3.16.0; python_version >= '3.7'", 'marshmallow-enum==1.5.1', 'mypy-extensions==0.4.3', 'orderedmultidict==1.0.1', "packaging==20.9; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", 'pep517==0.12.0', "pip==22.1.2; python_version >= '3.7'", "pip-shims==0.7.0; python_version >= '3.6'", 'pipenv-setup==3.2.0', 'pipfile==0.0.2', "platformdirs==2.5.2; python_version >= '3.7'", "plette[validation]==0.2.3; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'", "pluggy==1.0.0; python_version >= '3.6'", "py==1.11.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", 'pydash==5.1.0', "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'", 'pytest==7.1.2', "python-dateutil==2.8.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", "requests==2.28.0; python_version >= '3.7' and python_version < '4'", "requirementslib==1.6.4; python_version >= '3.7'", "setuptools==62.3.3; python_version >= '3.7'", "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", "toml==0.10.2; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'", "tomli==2.0.1; python_version >= '3.7'", "tomlkit==0.11.0; python_version >= '3.6' and python_version < '4'", "typing-extensions==4.2.0; python_version >= '3.7'", 'typing-inspect==0.7.1', "urllib3==1.26.9; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'", "vistir==0.5.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", "wheel==0.37.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'"],  # Optional
    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    extras_require={
        "dev": [
            "alabaster==0.7.12",
            "astroid==2.11.5; python_full_version >= '3.6.2'",
            "asttokens==2.0.5",
            "attrs==21.4.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "babel==2.10.1; python_version >= '3.6'",
            "beautifulsoup4==4.11.1; python_version >= '3.6'",
            "black==22.3.0",
            "cached-property==1.5.2",
            "cerberus==1.3.4",
            "certifi==2022.5.18.1; python_version >= '3.6'",
            "cfgv==3.3.1; python_full_version >= '3.6.1'",
            "chardet==4.0.0",
            "charset-normalizer==2.0.12; python_version >= '3'",
            "click==8.1.3; python_version >= '3.7'",
            "colorama==0.4.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "coverage==6.4",
            "css-html-js-minify==2.5.5",
            "dill==0.3.5.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6'",
            "distlib==0.3.4",
            "docutils==0.17.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "executing==0.8.3",
            "filelock==3.7.0; python_version >= '3.7'",
            "icecream==2.1.2",
            "identify==2.5.1; python_version >= '3.7'",
            "idna==3.3; python_version >= '3'",
            "imagesize==1.3.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "importlib-metadata==4.11.4; python_version < '3.10'",
            "isort==5.10.1; python_version < '4.0' and python_full_version >= '3.6.1'",
            "jinja2==3.1.2; python_version >= '3.7'",
            "lazy-object-proxy==1.7.1; python_version >= '3.6'",
            "lxml==4.8.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "markupsafe==2.1.1; python_version >= '3.7'",
            "mccabe==0.7.0; python_version >= '3.6'",
            "mypy-extensions==0.4.3",
            "nodeenv==1.6.0",
            "orderedmultidict==1.0.1",
            "packaging==20.9; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pathspec==0.9.0",
            "pep517==0.12.0",
            "pip-shims==0.7.0; python_version >= '3.6'",
            "pipenv-setup==3.2.0",
            "pipfile==0.0.2",
            "platformdirs==2.5.2; python_version >= '3.7'",
            "plette[validation]==0.2.3; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pre-commit==2.19.0",
            "pycodestyle==2.8.0",
            "pydocstyle==6.1.1",
            "pygments==2.12.0; python_version >= '3.6'",
            "pylint==2.13.9",
            "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "python-dateutil==2.8.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "python-slugify[unidecode]==6.1.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5'",
            "pytz==2022.1",
            "pyyaml==6.0; python_version >= '3.6'",
            "requests==2.27.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5'",
            "requirementslib==1.6.4; python_version >= '3.7'",
            "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "snowballstemmer==2.2.0",
            "soupsieve==2.3.2.post1; python_version >= '3.6'",
            "sphinx==4.5.0",
            "sphinx-material==0.0.35",
            "sphinx-rtd-theme==1.0.0",
            "sphinxcontrib-applehelp==1.0.2; python_version >= '3.5'",
            "sphinxcontrib-devhelp==1.0.2; python_version >= '3.5'",
            "sphinxcontrib-htmlhelp==2.0.0; python_version >= '3.6'",
            "sphinxcontrib-jsmath==1.0.1; python_version >= '3.5'",
            "sphinxcontrib-qthelp==1.0.3; python_version >= '3.5'",
            "sphinxcontrib-serializinghtml==1.1.5; python_version >= '3.5'",
            "text-unidecode==1.3",
            "toml==0.10.2; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "tomli==2.0.1; python_version < '3.11' and python_version >= '3.6'",
            "tomlkit==0.11.0; python_version >= '3.6' and python_version < '4.0'",
            "typing-extensions==4.2.0; python_version < '3.10'",
            "unidecode==1.3.4",
            "urllib3==1.26.9; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4.0'",
            "virtualenv==20.14.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "vistir==0.5.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "wheel==0.37.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "wrapt==1.14.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "zipp==3.8.0; python_version >= '3.7'",
        ]
    },  # Optional
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #
    # Sometimes you’ll want to use packages that are properly arranged with
    # setuptools, but are not published to PyPI. In those cases, you can specify
    # a list of one or more dependency_links URLs where the package can
    # be downloaded, along with some additional hints, and setuptools
    # will find and install the package correctly.
    # see https://python-packaging.readthedocs.io/en/latest/dependencies.html#packages-not-on-pypi
    #
    dependency_links=[],
    # If using Python 2.6 or earlier, then these have to be included in
    # MANIFEST.in as well.
    # package_data={"sample": ["package_data.dat"]},  # Optional
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[("my_data", ["data/data_file"])],  # Optional
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    # entry_points={"console_scripts": ["sample=sample:main"]},  # Optional
    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    project_urls={  # Optional
        "Bug Reports": "https://github.com/pypa/sampleproject/issues",
        "Funding": "https://donate.pypi.org",
        "Say Thanks!": "http://saythanks.io/to/example",
        "Source": "https://github.com/pypa/sampleproject/",
    },
    entry_points={
        "console_scripts": [
            "anonigod=anonimization_script.cli:cli"
        ]
    },
)