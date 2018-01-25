# project/_config.py


import os

# grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

# define the full path for the database
DATABASE = 'flasktaskr.db'
DATABASE_PATH = os.path.join(basedir, DATABASE)

CSRF_ENABLED = True
SECRET_KEY = 'myprecious'

# the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
# FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant
# overhead and will be disabled by default in the future.
# Set it to True or False to suppress this warning.
SQLALCHEMY_TRACK_MODIFICATIONS = False

# the debug mode
DEBUG = False
