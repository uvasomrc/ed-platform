DEBUG = False
TESTING = False
CORS_ENABLED = False
SECRET_KEY = 'ed_platform_key_of_deep_secret_knackwursts!'
SQLALCHEMY_DATABASE_URI = "postgresql://ed_user:ed_pass@localhost/ed_platform"

#: Default attribute map for single signon.
SSO_ATTRIBUTE_MAP = {
    'ADFS_AUTHLEVEL': (False, 'authlevel'),
    'ADFS_GROUP': (False, 'group'),
    'ADFS_LOGIN': (False, 'nickname'),
    'ADFS_ROLE': (False, 'role'),
    'ADFS_EMAIL': (False, 'email'),
    'ADFS_IDENTITYCLASS': (False, 'external'),
    'HTTP_SHIB_AUTHENTICATION_METHOD': (False, 'authmethod'),
}

SSO_LOGIN_URL = '/api/login'

