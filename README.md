# discovergy
Python module to query the Discovergy API. 

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
```
pip install -r "requirements.txt"
```

## Built With
* Python 3

## Use Module
* Clone repository: `git clone git@github.com:buzzn/discovergy.git`
* Import module: `from discovergy.discovergy import discovergy`

## Run Tests
* Setup virtual environment in root directory: 
```
virtualenv -p /path/to/python3/installation my_venv
source my_venv/bin/activate 
```
* Install module: `pip install .`
* Run tests: `python tests/test_discovergy.py`

## Acknowledgements
* [Discovergy API Documentation](https://api.discovergy.com/docs/)
* [pydiscovergy](https://github.com/jpbede/pydiscovergy)
