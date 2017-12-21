import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join("./", "TEST_DB")
TESTING = True
CORS_ENABLED = True
DEBUG = False
DEVELOPMENT = False

#: Default attribute map for single signon.
# This makes it a little easier to spoof the values that come back from
# Shibboleth.  One of the aspects of constructing custom headers is that
# they are automatically converted to META Keys, so we have to refer
# to them as that when pulling them out.  This is slightly different from
# the structure that actually comes back from Shibboleth.
SSO_ATTRIBUTE_MAP = {
    'HTTP_UID': (True, 'uid'), # dhf8r
    'HTTP_GIVENNAME': (False, 'givenName'), # Daniel
    'HTTP_MAIL': (False, 'email')  # dhf8r@Virginia.EDU
}

ELASTIC_SEARCH = {
    "index_prefix": "test",
    "hosts": ["localhost"],
    "port": 9200,
    "timeout": 20,
    "verify_certs": False,
    "use_ssl": False,
    "http_auth_user": "",
    "http_auth_pass": ""
}

MAIL_SERVER = 'localhost'
MAIL_PORT = 2525
MAIL_USE_TLS = False
MAIL_USE_SSL = False
#MAIL_USERNAME = "daniel.h.funk@gmail.com"
#MAIL_PASSWORD = "bmpnrbqmwvyfdjgb"
MAIL_DEFAULT_SENDER='daniel.h.funk@gmail.com'
MAIL_DEFAULT_RECIPIENT='daniel.h.funk@gmail.com'

# Use the isntance/config.py connection for now, but use
# a category and user_group that we can use to clear out any created data.0
DISCOURSE_CATEGORY = "test_posts"
DISCOURSE_USER_GROUP = "test_users"