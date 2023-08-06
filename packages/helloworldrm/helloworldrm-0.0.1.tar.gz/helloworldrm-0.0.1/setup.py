#setup.py
from setuptools import setup

with open("README.md", 'r') as fh:
    README = fh.read()

setup(
    name = 'helloworldrm', # pip install helloworld
    version = '0.0.1',
    description = 'Say Hello',
    #long_description_content_type="text/markdown",
    #long_description=README,
    py_modules = ['helloworld'], # Module name (file.py)
    package_dir = {'':'src'}, # Package name (folder)
    install_requires = [ # Install dependencies
        "streamlit",
        "check-manifest"
    ],
    extras_require = {
        "dev": [
            "pytest>=3.7",
            "tox",
            "twine",
            "wheel==0.30.0"
        ]
    },
    url = "https://github.com/joseignaciorm/python_package_example",
    author = "Nacho",
    author_email = "joseignaciorm13@gmail.com"
)

#1: To build the package running: python setup.py bdist_wheel \ 
    # python setup.py sdist (source distribution) has more data...
#2: Install it locally for testing: pip install -e . => Install this pkg in the current dir
#3: Check manifest
    # pip install check-manifest
    # check-manifest --create
    # git add MANIFEST.in

# Publish it!
# $python setup.py bdist_wheel sdist
# $ls dist/

# Push to PyPI
    # Stick this in extras_require
    # $pip install twine => Separate the build step from the upload step
    # $twine upload dist/* or twine upload dist/* --repository-url https://upload.pypi.org/legacy/ dist/* or twine upload --repository-url https://test.pypi.org/legacy/ dist/*
        #USERNAME: USER
        #password:

# tox.ini => pip install tox => run $tox
#[tox]
#envlist = py36,py37

#[testenv]
#deps = pytest
#commands = pytest
