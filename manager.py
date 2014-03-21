#!/usr/bin/env python
# coding: utf-8

from flask_script import Manager, Server
from collector.app import create_app

app = create_app()

manager = Manager(app)
manager.add_command('runserver', Server())

@manager.command
def createdb():
    """Create the database"""
    from collector.models import db

    db.create_all()

@manager.command
def createsitemap():
    """Create the sitemap"""
    from collector.commands.sitemap import Sitemap

    sitemap = Sitemap()
    sitemap.make()

@manager.command
def runtask(name=None):
    """Run task server"""
    from celery.bin.worker import worker
    from celery.bin.beat import beat

    log_level = app.config.get('CELERY_LOG_LEVEL')

    if name == 'celery':
        worker = worker(app=app.celery)
        worker.run(loglevel=log_level)
    elif name == 'beat':
        beat = beat(app=app.celery)
        beat.run(loglevel=log_level)
    elif name == 'all':
        worker = worker(app=app.celery)
        worker.run(loglevel=log_level, beat=True)
    else:
        print("Usage: python manager.py runtask -n [celery | beat | all]")

@manager.command
def fill(table=None):
    """Fill all the specified data into table"""

    from collector.commands import FillStream, FillToday, FillTodayDetail

    if table == "stream":
        fill_stream = FillStream()
        fill_stream.make()
    elif table == "today":
        fill_today = FillToday()
        fill_today.make()
    elif table == "todaydetail":
        fill_today_detail = FillTodayDetail()
        fill_today_detail.make()
    else:
        print("Usage: python manager.py fill -t [stream | today | todaydetail]")

@manager.command
def latest(table=None):
    """Fill latest and specified data into table"""

    from collector.commands import LatestStream, LatestToday, LatestTodayDetail

    if table == "stream":
        latest_stream = LatestStream()
        latest_stream.make()
    elif table == "today":
        latst_today = LatestToday()
        latst_today.make()
    elif table == "todaydetail":
        latest_today_detail = LatestTodayDetail()
        latest_today_detail.make()
    else:
        print("Usage: python manager.py latest -t [stream | today | todaydetail]")

if __name__ == '__main__':
    manager.run()
