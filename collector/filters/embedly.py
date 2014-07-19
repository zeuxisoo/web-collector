# coding: utf-8

import os
from flask import current_app, request

class Embedly(object):

    def __init__(self, token):
        self.token = token

    def fill(self, url, category, width, height, color, grow):
        url = self.fill_archive_url(url, category)

        api = 'https://i.embed.ly/1/display/fill'
        src = "{0}?key={1}&url={2}&width={3}&height={4}&color={5}&grow={6}"

        return src.format(api, self.token, url, width, height, color, grow)

    def fill_archive_url(self, url, category):
        if current_app.config.get('ARCHIVE') is True:
            url = "{0}/{1}/{2}/{3}".format(request.url_root[:-1], 'static/download/aria2c', category, os.path.basename(url))

        return url
