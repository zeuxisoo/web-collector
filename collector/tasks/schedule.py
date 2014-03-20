# coding: utf-8

# from __future__ import absolute_import

import importlib
from celery import task
from celery.utils.log import get_task_logger
from ..commands.sitemap import Sitemap
from ..commands.latest import LatestStream, LatestToday, LatestTodayDetail

logger = get_task_logger(__name__)

@task
def create_sitemap(offset, limit):
    logger.info("called schedule.create_sitemap, offset: {0}, limit: {1}".format(offset, limit))

    Sitemap(logger=logger).make(offset, limit)

@task
def create_latest(suffix_name):
    logger.info("called schedule.create_latest, suffix name: {0}".format(suffix_name))

    current_package = __name__.split('.')[0]
    command_modules = importlib.import_module(".commands", package=current_package)
    command_class   = getattr(command_modules, 'Latest{0}'.format(suffix_name))

    command_class(logger=logger).make()
