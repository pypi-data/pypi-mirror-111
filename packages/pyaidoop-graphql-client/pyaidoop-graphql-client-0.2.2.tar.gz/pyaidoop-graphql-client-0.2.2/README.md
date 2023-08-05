# vision-client-python
A graphql communication library for AIdoop web-based application platform such as AIdoop-R.
The library includes graphql client api and defines graphql query and mutations for AIdoop-R

## Setup
### setup commands
```
pip install -r requirements.txt
pip install --upgrade pip
python setup.py install
python setup.py sdist bdist_wheel
pip install twine
python -m twine upload dist/*
``` 

### test commands
- Prerequisites
  - run aidoop-r node servere before 
  - add appropriate connections with parameters in aidoop-r
```
cd test
python -m unittest 
```
