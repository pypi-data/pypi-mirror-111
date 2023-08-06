# flake8_loopy
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/) ![GitHub](https://img.shields.io/github/license/bdscharf/flake8_loopy) [![Build Status](https://www.travis-ci.com/bdscharf/flake8_loopy.svg?branch=main)](https://www.travis-ci.com/bdscharf/flake8_loopy) [![codecov](https://codecov.io/gh/bdscharf/flake8_loopy/branch/main/graph/badge.svg?token=NKEANWPS8P)](https://codecov.io/gh/bdscharf/flake8_loopy)

basic code quality checks in loops

```pip install flake8_loopy```

## checks
| error code      | description |
| ----------- | ----------- |
| LPY100      | unused variable created by ```enumerate()```: you probably do not need ```enumerate()```, or you should use ```range(len())``` instead      |
| LPY101      | variable created by for loop shadows a variable in its outer context                                                                        |

## future
- iteration with index where index is only used to get an item (should iterate directly over items)


## notes
please report false positives / errors if found! contributions welcome.