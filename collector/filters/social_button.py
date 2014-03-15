# coding: utf-8

from flask import request

class SocialButton(object):

    def __init__(self, config):
        self.config = config

    def create(self, text=None):
        enabled_socials = []
        for social, status in self.config['ids'].iteritems():
            if status:
                enabled_socials.append('data-{0}="{1}"'.format(social, status))

        template = '<div class="social-button" {0} data-count="{1}" data-text="{2}" data-url="{3}"></div>'

        if text is None or len(text) <= 0:
            text = self.config['text']

        return template.format(' '.join(enabled_socials), self.config['count'], text, request.url)
