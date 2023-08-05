# Varius
[![test](https://github.com/ChenchaoZhao/varius/actions/workflows/lint-test.yaml/badge.svg)](https://github.com/ChenchaoZhao/varius/actions/workflows/lint-test.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://pypip.in/v/varius/badge.png)](https://pypi.python.org/pypi/varius)

Perform computations using various versions of variables

Varius is the Latin word for "various."

## Install

`pip install varius`

## Usage Examples

```python
import varius
from varius import *

# default variables
cst = vr('cost [usd]', 100)
rev = vr('revenue [usd]', 300)

# expressions: if values are not given the expressions will be symbolic
pft = ex('profit [usd]', rev - cst)
pmg = ex('profit margin', pft.expr/rev)

# show() will display the variables or expressions based on your python env
# if in jupyter notebooks, they will be displayed as beautiful latex equations otherwise as plain texts

with note('default') as d:
    show(cst, rev, pft, pmg)
    print(d)

# new case
with note('20% discount', copy='default') as d:
    rev(rev['default'] * 0.8)
    show(cst, rev, pft, pmg)
    print(d)


# another case
with note('50% discount', copy='default') as d:
    rev(rev['default'] * 0.5)
    show(cst, rev, pft, pmg)
    print(d)

```

You will get summaries as follows:

```python
Scope version: default
  Variables:
    (cost [usd]) = 100
    (revenue [usd]) = 300
  Expressions:
    (profit [usd]) = 200
    (profit margin) = 2/3

Scope version: 20% discount
  Variables:
    (cost [usd]) = 100
    (revenue [usd]) = 240.0
  Expressions:
    (profit [usd]) = 140.000000000000
    (profit margin) = 0.5833333333333
    
Scope version: 50% discount
  Variables:
    (cost [usd]) = 100
    (revenue [usd]) = 150.0
  Expressions:
    (profit [usd]) = 50.0000000000000
    (profit margin) = 0.3333333333333
```
