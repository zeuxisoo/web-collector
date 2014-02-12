import os

DEBUG                      = True
SESSION_COOKIE_NAME        = '_s'
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30
SECRET_KEY                 = "Your_Secret_Key"

SQLALCHEMY_DATABASE_URI    = 'sqlite:///%s' % os.path.join(os.getcwd(), 'data', 'default.sqlite')