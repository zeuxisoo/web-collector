# coding: utf-8

from __future__ import absolute_import
import os
from flask import g
from celery import task
from dropbox import client
from ..models import UserConnection
from ..helpers.task import download_image

@task
def sync_image(category, user_id, result_id):
    print("called dropbox.save_to_dropbox, category: {0}, result id: {1}".format(category, result_id))

    saved_file      = download_image(category, result_id)
    user_connection = UserConnection.query.filter_by(user_id=user_id, provider_name='dropbox').first()

    print("==> saved_file: {0}".format(saved_file))
    print("==> user_connection: {0}".format('PASS' if user_connection.access_token != '' else 'Failed'))

    if saved_file and user_connection and user_connection.access_token != '':
        dropbox_client = client.DropboxClient(user_connection.access_token)

        dropbox_client.put_file(
            '/{0}/{1}'.format(category, os.path.basename(saved_file)),
            open(saved_file),
            overwrite=True
        )

        print("==> Saved")
    else:
        print("==> Failed")
