import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join("./", "TEST_DB")
TESTING = True
CORS_ENABLED = True
DEBUG = False
