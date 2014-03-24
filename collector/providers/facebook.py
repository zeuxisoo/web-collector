# coding: utf-8

from __future__ import absolute_import
import facebook

class FacebookProvider(object):

    def __init__(self, access_token):
        self.access_token = access_token
        self.oauth_client = facebook.GraphAPI(access_token)
        self.account_info = self.oauth_client.get_object('me')

    def user_id(self):
        return self.account_info['id']

    def display_name(self):
        return '{0} {1}'.format(self.account_info['last_name'], self.account_info['first_name'])

    def email(self):
        return self.account_info['email']
