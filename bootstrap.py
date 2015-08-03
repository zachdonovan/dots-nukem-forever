from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)

directory = 'tmp/'
if not os.path.exists(directory):
     os.makedirs(directory)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/test.db'
db = SQLAlchemy(app)

def get_db():
  global db
  return db
