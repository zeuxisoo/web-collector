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
