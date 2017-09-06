DEBUG = False
TESTING = False
CORS_ENABLED = False
SECRET_KEY = 'ed_platform_key_of_deep_secret_knackwursts!'
SQLALCHEMY_DATABASE_URI = "postgresql://ed_user:ed_pass@localhost/ed_platform"

#: Default attribute map for single signon.
SSO_ATTRIBUTE_MAP = {
    'eppn': (True, 'eppn'),  # dhf8r@virginia.edu
    'uid': (False, 'uid'),  # dhf8r
    'givenName': (False, 'givenName'), # Daniel
    'mail': (False, 'email'), # dhf8r@Virginia.EDU
    'sn': (False, 'surName'), # Funk
    'affiliation': (False, 'affiliation'), #  'staff@virginia.edu;member@virginia.edu'
    'displayName': (False, 'displayName'), # Daniel Harold Funk
    'title': (False, 'title')  # SOFTWARE ENGINEER V
}


SSO_LOGIN_URL = '/api/login'

