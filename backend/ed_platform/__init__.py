import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_sso import SSO
from flask_uploads import UploadSet, configure_uploads
from flask_compress import Compress

from ed_platform.elastic_index import ElasticIndex
from ed_platform.notify import Notify
from ed_platform.rest_exception import RestException
from ed_platform.discourse import Discourse


compress = Compress()

app = Flask(__name__, instance_relative_config=True)

# add compression.
compress.init_app(app)

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

# Set the secret key from the configuration file.
app.secret_key = app.config['SECRET_KEY']

# Set up Single sign-on.
sso = SSO(app=app)

# Sending email messages.
notify = Notify(app)

# Search System
elastic_index = ElasticIndex(app)

# Discourse Connection
discourse = Discourse(app)

# Uploaded Files
profile_photos = UploadSet('photos')
configure_uploads(app, (profile_photos))

# Handle errors consistently
@app.errorhandler(RestException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(404)
def handle_404(error):
    return handle_invalid_usage(RestException(RestException.NOT_FOUND, 404))


from ed_platform import models
from ed_platform import views
