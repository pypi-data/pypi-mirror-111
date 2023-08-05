# pyannotators_keybert

[![license](https://img.shields.io/github/license/oterrier/pyannotators_keybert)](https://github.com/oterrier/pyannotators_keybert/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyannotators_keybert/workflows/tests/badge.svg)](https://github.com/oterrier/pyannotators_keybert/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyannotators_keybert)](https://codecov.io/gh/oterrier/pyannotators_keybert)
[![docs](https://img.shields.io/readthedocs/pyannotators_keybert)](https://pyannotators_keybert.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyannotators_keybert)](https://pypi.org/project/pyannotators_keybert/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyannotators_keybert)](https://pypi.org/project/pyannotators_keybert/)

Annotator based on Facebook's KeyBERT

## Installation

You can simply `pip install pyannotators_keybert`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyannotators_keybert
```

### Running the test suite

You can run the full test suite against all supported versions of Python (3.8) with:

```
tox
```

### Building the documentation

You can build the HTML documentation with:

```
tox -e docs
```

The built documentation is available at `docs/_build/index.html.
