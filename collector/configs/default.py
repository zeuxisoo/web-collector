# coding: utf-8

import os
from celery.schedules import crontab

# SERVER_NAME                = 'localhost'
# ARCHIVE                    = True
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

FACEBOOK = {
    'consumer_key'        : '144059545617481',
    'consumer_secret'     : 'be3e4ae0013f6c7526ef3dc153ed412d',
    'request_token_params': {'scope': 'email'},
    'base_url'            : 'https://graph.facebook.com',
    'request_token_url'   : None,
    'access_token_method' : 'POST',
    'access_token_url'    : '/oauth/access_token',
    'authorize_url'       : 'https://www.facebook.com/dialog/oauth',
}

BROKER_URL                   = 'redis://localhost:6379/0',
CELERY_RESULT_BACKEND        = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT        = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER       = 'json'
CELERY_RESULT_SERIALIZER     = 'json'
CELERY_LOG_LEVEL             = 'INFO'
# CELERYD_LOG_FILE             = os.path.join(os.getcwd(), 'data/celeryd.log')
CELERY_TIMEZONE              = 'Asia/Hong_Kong'
CELERYBEAT_SCHEDULE_FILENAME = os.path.join(os.getcwd(), 'data/celery-beat')
CELERYBEAT_SCHEDULE          = {
    'create-sitemap-all': {
        'task': 'collector.tasks.schedule.create_sitemap',
        'schedule': crontab(minute=0, hour='*/3'), # every three hours
        'args': (0, 10000)
    },
    # 'create-latest-stream': {
    #     'task': 'collector.tasks.schedule.create_latest',
    #     'schedule': crontab(minute='*/15'), # every 15 minute
    #     'args': ('Stream',)
    # },
    # 'create-latest-today': {
    #     'task': 'collector.tasks.schedule.create_latest',
    #     'schedule': crontab(minute=0, hour=0), # every daily at 00:00
    #     'args': ('Today',)
    # },
    # 'create-latest-todaydetail': {
    #     'task': 'collector.tasks.schedule.create_latest',
    #     'schedule': crontab(minute=3, hour=0), # every daily at 00:03
    #     'args': ('TodayDetail',)
    # }
}

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

GRAVATAR_BASE_URL = 'http://www.gravatar.com/avatar/'
GRAVATAR_EXTRA    = ''

GOOGLE_ANALYTICS    = ''
GOOGLE_ANALYTICS_DC = False

GOOGLE_ADSENSE = {
    'client'   : 'ca-pub-XXXXX',
    'slidebar' : dict(enable=False, slot=''),
    'footer'   : dict(enable=False, slot='')
}

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

EXTERNAL_LINKS = {
    # 'name': "url"
}
