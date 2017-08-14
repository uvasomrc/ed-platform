import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import *

app = Flask(__name__, instance_relative_config=True)

# Load configuration
app.config.from_object('config')
app.config.from_pyfile('config.py')

# Enable CORS
if(app.config["CORS_ENABLED"]) :
    cors = CORS(app, resources={r"*": {"origins": "*"}})

# Database Configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from ed_platform import models
from ed_platform import views