# coding: utf-8

import datetime

class Clock(object):
    def humanize(self, value):
        now   = datetime.datetime.utcnow()
        delta = now - value

        if delta.days > 365:
            return '{num} years ago'.format(num=delta.days / 365)

        if delta.days > 30:
            return '{num} months ago'.format(num=delta.days / 30)

        if delta.days > 0:
            return '{num} days ago'.format(num=delta.days)

        if delta.seconds > 3600:
            return '{num} hours ago'.format(num=delta.seconds / 3600)

        if delta.seconds > 60:
            return '{num} minutes ago'.format(num=delta.seconds / 60)

        return 'just now'


    def xml_format(self, value):
        if not isinstance(value, datetime.datetime):
            return value
        else:
            return value.strftime('%Y-%m-%dT%H:%M:%SZ')
