DEBUG = True
TESTING = False
CORS_ENABLED = False
DEVELOPMENT = False
SECRET_KEY = 'ed_platform_key_of_deep_secret_knackwursts!'
SQLALCHEMY_DATABASE_URI = "postgresql://ed_user:ed_pass@localhost/ed_platform"

#: Default attribute map for single signon.
SSO_DEVELOPMENT_UID = 'bk7k'
SSO_ATTRIBUTE_MAP = {
    'eppn': (False, 'eppn'),  # dhf8r@virginia.edu
    'uid': (True, 'uid'),  # dhf8r
    'givenName': (False, 'givenName'), # Daniel
    'mail': (False, 'email'), # dhf8r@Virginia.EDU
    'sn': (False, 'surName'), # Funk
    'affiliation': (False, 'affiliation'), #  'staff@virginia.edu;member@virginia.edu'
    'displayName': (False, 'displayName'), # Daniel Harold Funk
    'title': (False, 'title')  # SOFTWARE ENGINEER V
}

API_URL = "http://localhost:5000"
SITE_URL = "http://localhost:4200"


FRONTEND_AUTH_CALLBACK = "http://localhost:4200/#/account"
SSO_LOGIN_URL = '/api/login'

# email server
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
#MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = ""
MAIL_PASSWORD = ""
MAIL_DEFAULT_SENDER='daniel.h.funk@gmail.com'

