`hypothesis` strategies for `SQLAlchemy`
========================================

[![](https://travis-ci.org/lycantropos/hypothesis_sqlalchemy.svg?branch=master)](https://travis-ci.org/lycantropos/hypothesis_sqlalchemy "Travis CI")
[![](https://dev.azure.com/lycantropos/hypothesis_sqlalchemy/_apis/build/status/lycantropos.hypothesis_sqlalchemy?branchName=master)](https://dev.azure.com/lycantropos/hypothesis_sqlalchemy/_build/latest?branchName=master "Azure Pipelines")
[![](https://codecov.io/gh/lycantropos/hypothesis_sqlalchemy/branch/master/graph/badge.svg)](https://codecov.io/gh/lycantropos/hypothesis_sqlalchemy "Codecov")
[![](https://img.shields.io/github/license/lycantropos/hypothesis_sqlalchemy.svg)](https://github.com/lycantropos/hypothesis_sqlalchemy/blob/master/LICENSE "License")
[![](https://badge.fury.io/py/hypothesis-sqlalchemy.svg)](https://badge.fury.io/py/hypothesis-sqlalchemy "PyPI")

In what follows
- `python` is an alias for `python3.5` or any later
version (`python3.6` and so on),
- `pypy` is an alias for `pypy3.5` or any later
version (`pypy3.6` and so on).

Installation
------------

Install the latest `pip` & `setuptools` packages versions:
- with `CPython`
  ```bash
  python -m pip install --upgrade pip setuptools
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --upgrade pip setuptools
  ```

### User

Download and install the latest stable version from `PyPI` repository:
- with `CPython`
  ```bash
  python -m pip install --upgrade hypothesis_sqlalchemy
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --upgrade hypothesis_sqlalchemy
  ```

### Developer

Download the latest version from `GitHub` repository
```bash
git clone https://github.com/lycantropos/hypothesis_sqlalchemy.git
cd hypothesis_sqlalchemy
```

Install dependencies:
- with `CPython`
  ```bash
  python -m pip install -r requirements.txt
  ```
- with `PyPy`
  ```bash
  pypy -m pip install -r requirements.txt
  ```

Install:
- with `CPython`
  ```bash
  python setup.py install
  ```
- with `PyPy`
  ```bash
  pypy setup.py install
  ```

Usage
-----

Let's take a look at what can be generated and how.

### Tables

We can write a strategy that produces tables
```python
>>> from hypothesis import strategies
>>> from hypothesis_sqlalchemy import tabular
>>> from sqlalchemy.schema import MetaData
>>> tables = tabular.factory(metadatas=strategies.builds(MetaData),
...                          min_size=3,
...                          max_size=10)
>>> table = tables.example()
>>> from sqlalchemy.schema import Table
>>> isinstance(table, Table)
True
>>> from sqlalchemy.schema import Column
>>> all(isinstance(column, Column) for column in table.columns)
True
>>> 3 <= len(table.columns) <= 10
True

```

### Records

Suppose we have a table
```python
>>> from sqlalchemy.schema import (Column,
...                                MetaData,
...                                Table)
>>> from sqlalchemy.sql.sqltypes import (Integer,
...                                      String)
>>> metadata = MetaData()
>>> user_table = Table('user', metadata,
...                    Column('user_id', Integer,
...                           primary_key=True),
...                    Column('user_name', String(16),
...                           nullable=False),
...                    Column('email_address', String(60)),
...                    Column('password', String(20),
...                           nullable=False))

```
and we can write strategy that
* produces single records (as `tuple`s)
    ```python
    >>> from hypothesis import strategies
    >>> from hypothesis_sqlalchemy import tabular
    >>> records = tabular.records.factory(user_table, 
    ...                                   email_address=strategies.emails())
    >>> record = records.example()
    >>> isinstance(record, tuple)
    True
    >>> len(record) == len(user_table.columns)
    True
    >>> all(column.nullable and value is None
    ...     or isinstance(value, column.type.python_type) 
    ...     for value, column in zip(record, user_table.columns))
    True
  
    ```
* produces records `list`s (with configurable `list` size bounds)
    ```python
    >>> from hypothesis_sqlalchemy import tabular
    >>> records_lists = tabular.records.lists_factory(user_table,
    ...                                               min_size=2,
    ...                                               max_size=5, 
    ...                                               email_address=strategies.emails())
    >>> records_list = records_lists.example()
    >>> isinstance(records_list, list)
    True
    >>> 2 <= len(records_list) <= 5
    True
    >>> all(isinstance(record, tuple) for record in records_list)
    True
    >>> all(len(record) == len(user_table.columns) for record in records_list)
    True

    ```

Development
-----------

### Bumping version

#### Preparation

Install
[bump2version](https://github.com/c4urself/bump2version#installation).

#### Pre-release

Choose which version number category to bump following [semver
specification](http://semver.org/).

Test bumping version
```bash
bump2version --dry-run --verbose $CATEGORY
```

where `$CATEGORY` is the target version number category name, possible
values are `patch`/`minor`/`major`.

Bump version
```bash
bump2version --verbose $CATEGORY
```

This will set version to `major.minor.patch-alpha`. 

#### Release

Test bumping version
```bash
bump2version --dry-run --verbose release
```

Bump version
```bash
bump2version --verbose release
```

This will set version to `major.minor.patch`.

### Running tests

Install dependencies:
- with `CPython`
  ```bash
  python -m pip install -r requirements-tests.txt
  ```
- with `PyPy`
  ```bash
  pypy -m pip install -r requirements-tests.txt
  ```

Plain
```bash
pytest
```

Inside `Docker` container:
- with `CPython`
  ```bash
  docker-compose --file docker-compose.cpython.yml up
  ```
- with `PyPy`
  ```bash
  docker-compose --file docker-compose.pypy.yml up
  ```

`Bash` script (e.g. can be used in `Git` hooks):
- with `CPython`
  ```bash
  ./run-tests.sh
  ```
  or
  ```bash
  ./run-tests.sh cpython
  ```

- with `PyPy`
  ```bash
  ./run-tests.sh pypy
  ```

`PowerShell` script (e.g. can be used in `Git` hooks):
- with `CPython`
  ```powershell
  .\run-tests.ps1
  ```
  or
  ```powershell
  .\run-tests.ps1 cpython
  ```
- with `PyPy`
  ```powershell
  .\run-tests.ps1 pypy
  ```
