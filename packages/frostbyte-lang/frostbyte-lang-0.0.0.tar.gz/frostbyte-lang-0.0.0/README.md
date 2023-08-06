# Frostbyte

[![Generic badge](https://img.shields.io/badge/python-3.9+-green.svg)](https://docs.python.org/3.9/)
[![Generic badge](https://img.shields.io/badge/mypy-checked-blue)](https://github.com/python/mypy)
[![PyPI version shields.io](https://img.shields.io/pypi/v/frostbyte-core.svg)](https://pypi.python.org/pypi/frostbyte-core/)
[![PyPI status](https://img.shields.io/pypi/status/frostbyte-core.svg)](https://pypi.python.org/pypi/frostbyte-core/)

This is the reference implementation for the Frostbyte programming language and smart contract protocol. You can install the latest release from PyPI as follows:

```
pip install frostbyte-lang
```

The documentation for this project is automatically generated using [pdoc](https://github.com/pdoc3/pdoc) and can be found in the [docs folder](./docs).

## Running a Frostbyte node

The library includes scripts that automate the process of setting up and running a Frostbyte node. To set up a new node, run the command below in your terminal and follow the instructions:

```
frostbyte-setup
```

After you completed the setup, you can start a node by running the command below in your terminal:

```
frostbyte-run
```

If you wish to modify the configuration for a node, run the command below in your terminal and follow the instructions:

```
frostbyte-config
```

These command line utilities have a number of 

## The Frostbyte programming language

Frostbyte is implemented as an [embedded domain-specific language (eDSL)](https://en.wikipedia.org/wiki/Domain-specific_language#External_and_Embedded_Domain_Specific_Languages), with Python as its host language. Frostbyte objects&mdash;including contracts, tokens and transactions&mdash;are constructed and processed by running Python scripts written using this eDSL.

As a matter of convention, all Frostbyte types and functions should be imported from the `frostbyte` module at the beginning of the script (or notebook):

```py
from frostbyte import *
```

In the rest of this document, we cover the basics of smart contract programming and execution in Frostbyte. A full reference for the language is provided by the [Frostbyte whitepaper](github.com/frostbyte-lang/whitepaper). Detailed examples can be found in the [notebooks folder](./notebooks) folder.

