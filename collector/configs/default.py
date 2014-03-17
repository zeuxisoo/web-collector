# coding: utf-8

import os

DEBUG                      = True
SESSION_COOKIE_NAME        = '_s'
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30
SECRET_KEY                 = "Your_Secret_Key"

SQLALCHEMY_DATABASE_URI    = 'sqlite:///%s' % os.path.join(os.getcwd(), 'data', 'default.sqlite')

EMBEDLY_API_TOKEN          = '4d1f889c20ed11e1abb14040d3dc5c07'
CURATORS_API_TOKEN         = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'

DROPBOX = {
    'consumer_key'        : 'xvl67yuz9wxsv5g',
    'consumer_secret'     : 'ja7lrm66jva1xsx',
    'request_token_params': {},
    'base_url'            : 'https://www.dropbox.com/1/',
    'request_token_url'   : None,
    'access_token_method' : 'POST',
    'access_token_url'    : 'https://api.dropbox.com/1/oauth2/token',
    'authorize_url'       : 'https://www.dropbox.com/1/oauth2/authorize',
}

BROKER_URL               = 'redis://localhost:6379/0',
CELERY_RESULT_BACKEND    = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT    = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER   = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_LOG_LEVEL         = 'INFO'

IMAGE_DOWNLOAD_PATH = os.path.join(os.getcwd(), 'static/download')

SOCIAL_BUTTON = {
    'ids': {
        'twitter' : 'zeuxisoo',
        'facebook': 'zeuxisoo',
        'weibo'   : 'zeuxisoo'
    },
    'count': True,
    'text' : 'Would you like to collector the girls? See ? Come here !!'
}

GOOGLE_ANALYTICS = ''

ADDTHIS = {
    'enable'   : True,
    'facebook' : True,
    'twitter'  : True,
    'google'   : True,
    'sinaweibo': True,
    'plurk'    : True,
    'pinterest': True,
    'pubid'    : '',
}

FACEBOOK_COMMENT = {
    'enable'     : True,
    'colorscheme': 'light',
    'order_by'   : 'social'
}
