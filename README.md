# flasktaskr

[![Build Status](https://travis-ci.org/zuzhi/flasktaskr.svg?branch=master)](https://travis-ci.org/zuzhi/flasktaskr)

A Flask App

## Install

```bash
# Create a virtual environment
$ python3 -m venv venv

# Enable it
$ source venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt
```

## Test

```bash
# Run tests
$ nosetests -v
```

## Run

```bash
# Run with development server
$ FLASK_APP=run.py FLASK_ENV=development flask run
```

## Develop

- Python Environment
- DB

## Deploy

- Travis-CI
- Heroku

## Some notes

Update heroku api_key

```bash
$ travis setup heroku --force
```

## TODO

- Update this README using https://github.com/pallets/flask/blob/master/examples/tutorial/README.rst as a reference.
