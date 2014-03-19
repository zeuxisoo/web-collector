# coding: utf-8

from __future__ import absolute_import
from os import path
from datetime import datetime
from flask import g, current_app, url_for, render_template
from ..models import Stream, Today
from celery import task

@task
def create_all(offset, limit):
    print("called sitemap.create_all, offset: {0}, limit: {1}".format(offset, limit))

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
    save_path = path.join(current_app.static_folder, 'siemap.xml')

    print("===> creating sitemap.xml to {0}".format(save_path))

    with open(save_path, 'w') as f:
        f.write(sitemap)
        f.close()

    return None
