import os

from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from config import *

app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config.default')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
if "APP_CONFIG_FILE" in os.environ:
    app.config.from_envvar('APP_CONFIG_FILE')


# Enable CORS
if(app.config["CORS_ENABLED"]) :
    cors = CORS(app, resources={r"*": {"origins": "*"}})

# Database Configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Set up Marshmallow for HATEOAS goodness (must happen after db)
ma = Marshmallow(app)

from ed_platform import models
from ed_platform import views
