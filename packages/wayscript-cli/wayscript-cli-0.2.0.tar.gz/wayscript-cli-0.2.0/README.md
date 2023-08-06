# WayScript CLI

## Environment Setup

Install Python 3.8.5 or later:

https://www.python.org/downloads/mac-osx/

If you don't already have it installed, install virtualenv:
```
sudo pip3.8 install virtualenv
```

Change to the project directory:
```
cd wayscript-cli
```

Create a new virtualenv using python3:
```
virtualenv -p /path/to/python3.8 venv
```
💡 Find `/path/to/python3.8` using `which python3.8`

Activate the new environment:
```
source venv/bin/activate
```

Install the dependencies:
```
pip install -r requirements.txt
```

Freeze with new dependencies:
```
pip freeze > requirements.txt
```

To install the actual local source so you can run it with `wayscript ...` run the following command (while still in virtual env):

```
pip install --editable .
```

## Run Tests

```
python test.py
```

## Run Coverage

```
coverage run test.py && coverage html
```
Then open ```htmlcov/index.html``` in your browser.


## Bundle and publish CLI build

Be sure to bump the cli version in `setup.py` first. Please adhere to semantic versioning.

```
python3 -m build

# for uploading to test PyPI use "--repository testpypi"
python3 -m twine upload dist/*
# you will be prompted for credentials, use __token__ as username, and for password use API token from PyPI
```

## Download CLI from Test PyPI

```
pip install wayscript-cli --extra-index-url=https://test.pypi.org/simple/
```
