# coding: utf-8

class Embedly(object):

    def __init__(self, token):
        self.token = token

    def fill(self, url, width, height, color, grow):
        api = 'https://i.embed.ly/1/display/fill'
        src = "{0}?key={1}&url={2}&width={3}&height={4}&color={5}&grow={6}"

        return src.format(api, self.token, url, width, height, color, grow)
