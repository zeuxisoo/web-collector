# coding: utf-8

# from __future__ import absolute_import

from celery import task
from celery.utils.log import get_task_logger
from ..commands.sitemap import Sitemap

logger = get_task_logger(__name__)

@task
def create_sitemap(offset, limit):
    logger.info("called schedule.create_sitemap, offset: {0}, limit: {1}".format(offset, limit))

    Sitemap(logger=logger).make(offset, limit)
