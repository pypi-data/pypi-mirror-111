# apitorch.py

> API Torch client written in python.

**Introduction**

API Torch is a platform that allows you to use, create, and deploy image classifiers.

---

## Getting Started

### Prerequisites

Register for a free account and have your API key handy. You can find your API key [here](https://www.apitorch.com/account).

### Installation

Add `apitorch` to your `requirements.txt`:

```
$ echo "apitorch" >> requirements.txt
```

Or install using pip:

```
pip install apitorch
```

### Configuration

Your API key should be in the environment variable `APITORCH_API_KEY`.

If you're in a Jupyter/Colab notebook environment, you may set environment variables using magics:

```
%env APITORCH_API_KEY your_api_key_here
```

If you cannot change environment variables on your system for some reason, you may manually set your API key:

```python
from apitorch.utils import set_api_key

set_api_key('YOUR API KEY')
```

### Make your first request

You may test your connection end-to-end by starting with a file `app.py` and adding the following code:

```python
from apitorch.ping import ping_api

response = ping_api()
assert response
```

Invoking the Python code by running `python app.py` should exit cleanly, without an assertion error.

## Documentation

Official API Documentation can be found at [https://docs.apitorch.com](https://docs.apitorch.com/?python).


## Debugging

By default, logging is set to `INFO`. You may change the log level:

```python
import logging
from apitorch.utils import set_log_level

set_log_level(logging.DEBUG)
```

## Development

Use `pyenv` to ensure you install the python version specified in [.python-version](.python-version). 

Install a virtual environemt: `python -v venv venv/`

Activate environment: `source venv/bin/activate`

Install dependencies: `pip install -r requirements-dev.txt`

### Testing

To run unit tests: `pytest`

To skip a test, decorate a function like so:

```
import pytest

@pytest.mark.skip(reason="Not yet implemented")
def test_something():
  # this function will not run
  raise Exception()
```

### Building

Ensure build module is installed: `python -m pip install build`

Build: `python -m build`

### Deploying package

```
twine check dist/apitorch-VERSION*

# deploy to test pypi repository
twine upload --repository testpypi dist/*

# deploy to production pypi repository
twine upload dist/apitorch-VERSION*
```