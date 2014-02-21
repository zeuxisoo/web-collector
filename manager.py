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

if __name__ == '__main__':
    manager.run()
