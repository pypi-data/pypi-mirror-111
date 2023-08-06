# coding=utf-8
# Copyright (c) Qotto, 2021

from os import path

import toml
import pipfile
from pipfile.api import PipfileParser
from setuptools import setup, find_packages

# Read long_description in README.md
# -----------------------------------------------------------------------------
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read dependencies in Pipfile
# -----------------------------------------------------------------------------
parsed_pipfile = PipfileParser(path.join(this_directory, 'Pipfile')).parse()
install_requires = list()
extra_requires = dict()
for pkg, ver in parsed_pipfile.get('default').items():
    if isinstance(ver, str):
        # default
        install_requires.append(f'{pkg}{ver}' if ver != "*" else pkg)
    else:
        # extra
        extra_requires[pkg] = [f'{p}{v}' if v != "*" else p for p, v in ver.items()]
extra_requires['develop'] = [f'{p}{v}' if v != "*" else p for p, v in parsed_pipfile.get('develop').items()]

# Setup
# See: https://packaging.python.org/guides/distributing-packages-using-setuptools/
# -----------------------------------------------------------------------------
setup(
    name="eventy",

    version="3.0.7",

    # https://packaging.python.org/specifications/core-metadata/#summary
    description="Qotto/eventy",

    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=long_description,

    long_description_content_type='text/markdown',

    # This field corresponds to the "Home-Page" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    url="https://gitlab.com/qotto/oss/eventy",

    # This should be your name or the name of the organization which owns the project.
    author="Qotto dev team",

    # This should be a valid email address corresponding to the author listed
    # above.
    author_email="dev@qotto.net",  # Optional

    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        # "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        # "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # These classifiers are *not* checked by 'pip install'. See instead
        # 'python_requires' below.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],

    # Note that this is a string of words separated by whitespace, not a list.
    # keywords="sample setuptools development",

    packages=find_packages(exclude=["docs", "tests", "recipes", "examples"]),

    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires=">=3.7, <4",

    # https://packaging.python.org/en/latest/requirements.html
    install_requires=install_requires,

    extras_require=extra_requires,

    # see https://python-packaging.readthedocs.io/en/latest/dependencies.html#packages-not-on-pypi
    dependency_links=[],

    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    project_urls={  # Optional
        "Qotto": "http://www.qotto.net",
        "Documentation": "https://qotto.gitlab.io/oss/eventy",
        "Source": "https://gitlab.com/qotto/oss/eventy",
        "Bug Reports": "https://gitlab.com/qotto/oss/eventy/-/issues",
    },
)
