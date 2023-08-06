# Hello World

This is an example project demostrating how to publish a python module to PyPI.


## Installation
Run the following to install:
```python
pip install helloworld
```

## Usage
```python
from helloworld import say_hello

# Genarate "Hello World!"
say_hello()

# Genarate "Hello, Everybody!"
say_hello("Hello, Everybody!" )
```

# Developing Hello World
To install helloworld, along with the tool need to develop and run test, run the following in your virtualenv:

```bash
$pip install -e .[dev]
```