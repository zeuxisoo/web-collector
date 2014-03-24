# coding: utf-8

from __future__ import absolute_import
import os
from flask import g
from celery import task
from celery.utils.log import get_task_logger
from dropbox import client
from ..models import UserConnection, DropboxLog
from ..helpers.task import download_image

logger = get_task_logger(__name__)

@task
def sync_image(category, user_id, result_id):
    logger.info("called dropbox.save_to_dropbox, category: {0}, result id: {1}".format(category, result_id))

    saved_file      = download_image(category, result_id)
    user_connection = UserConnection.query.filter_by(user_id=user_id, provider_name='dropbox').first()
    status          = 'faield'

    logger.info("==> saved_file: {0}".format(saved_file))
    logger.info("==> user_connection: {0}".format('PASS' if user_connection.access_token != '' else 'Failed'))

    if saved_file and user_connection and user_connection.access_token != '':
        dropbox_client = client.DropboxClient(user_connection.access_token)

        dropbox_client.put_file(
            '/{0}/{1}'.format(category, os.path.basename(saved_file)),
            open(saved_file),
            overwrite=True
        )

        status = 'success'

        logger.info("==> Saved")
    else:
        logger.info("==> Failed")

    DropboxLog(
        category  = category,
        user_id   = user_id,
        target_id = result_id,
        status    = status,
    ).save()
