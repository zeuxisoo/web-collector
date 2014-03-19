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

@manager.option('-n', '--name', help='Run task server')
def runtask(name):
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

@manager.option('-t', '--table', help='Fill the table')
def fill(table):
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

@manager.option('-t', '--table', help="Cron the table")
def cron(table):
    """Fill latest and specified data into table"""

    from collector.commands import CronStream, CronToday, CronTodayDetail

    if table == "stream":
        cron_stream = CronStream()
        cron_stream.make()
    elif table == "today":
        cron_today = CronToday()
        cron_today.make()
    elif table == "todaydetail":
        cron_today_detail = CronTodayDetail()
        cron_today_detail.make()
    else:
        print("Usage: python manager.py cron -t [stream | today | todaydetail]")

if __name__ == '__main__':
    manager.run()
