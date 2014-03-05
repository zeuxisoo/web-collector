#!/usr/bin/env python
# coding: utf-8

from flask_script import Manager, Server
from collector.app import create_app

app = create_app()

manager = Manager(app)
manager.add_command('runserver', Server())

@manager.command
def createdb():
    """ Create the database """
    from collector.models import db

    db.create_all()

@manager.command
def fillstream():
    """ Fill the stream table """
    from collector.command import FillStream

    fill_stream = FillStream()
    fill_stream.make()

@manager.command
def filltoday():
    """ Fill the today table """
    from collector.command import FillToday

    fill_today = FillToday()
    fill_today.make()

@manager.command
def filltodaydetail():
    """ Fill the today detail table """
    from collector.command import FillTodayDetail

    fill_today_detail = FillTodayDetail()
    fill_today_detail.make()

@manager.command
def runcelery():
    """Run celery."""
    from celery.bin.worker import worker

    worker = worker(app=app.celery)
    worker.run(loglevel=app.config.get('CELERY_LOG_LEVEL'))

@manager.command
def cronstream():
    """ Run cron job to get latest stream """
    from collector.command import CronStream

    cron_stream = CronStream()
    cron_stream.make()

@manager.command
def crontoday():
    """ Run cron job to get latest today """
    from collector.command import CronToday

    cron_today = CronToday()
    cron_today.make()

if __name__ == '__main__':
    manager.run()
