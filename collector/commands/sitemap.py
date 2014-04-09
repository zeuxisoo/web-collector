# coding: utf-8

from os import path
from datetime import datetime
from flask import g, current_app, url_for, render_template
from ..models import Stream, Today
from .base import BaseCommand

class Sitemap(BaseCommand):

    def __init__(self, logger=None):
        self.logger = self.get_logger() if logger is None else logger

        self.logger.info("Sitemap")

    def make(self, offset=0, limit=10000):
        streams = Stream.query.order_by(Stream.result_created_at.desc()).offset(offset).limit(limit).all()
        todays  = Today.query.order_by(Today.result_date.desc()).offset(offset).limit(limit).all()

        pages = []

        for stream in streams:
            pages.append({
                'url'      : url_for('stream.detail', result_id=stream.result_id, name=stream.result_name, _external=True),
                'image'    : stream.result_image,
                'create_at': stream.result_created_at.isoformat(),
            })

        for today in todays:
            pages.append({
                'url'      : url_for('today.detail', result_date=today.result_date, result_id=today.result_id, name=today.result_name, _external=True),
                'image'    : today.result_image,
                'create_at': datetime.combine(today.result_date, datetime.min.time()).isoformat(),
            })

        sitemap   = render_template('sitemap.xml', pages=pages)
        save_path = path.join(current_app.static_folder, 'sitemap.xml')

        self.logger.info("===> creating sitemap.xml to {0}".format(save_path))

        with open(save_path, 'w') as f:
            f.write(sitemap)
            f.close()


