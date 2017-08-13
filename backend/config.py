import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CORS_ENABLED = False
    SECRET_KEY = 'ed_platform_key_of_deep_secret_knackwursts!'
    SQLALCHEMY_DATABASE_URI = "postgresql://ed_user:ed_pass@localhost/ed_platform"

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    CORS_ENABLED = True
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join("./", "TEST_DB")
    TESTING = True
    CORS_ENABLED= True
    DEBUG = False


