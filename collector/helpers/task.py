# coding: utf-8

import os
import errno
import requests
from flask import current_app
from ..models import Stream, Today

def mkdirs(directory):
    try:
        os.makedirs(directory)
    except OSError as err:
        if err.errno == errno.EEXIST and os.path.isdir(directory):
            pass

def download_image(category, result_id):
    if category == 'stream':
        Model  = Stream
        folder = 'stream'
    elif category == 'today':
        Model  = Today
        folder = 'today'
    else:
        return None

    row = Model.query.filter_by(result_id=result_id).first()

    if row:
        image_path = current_app.config.get('IMAGE_DOWNLOAD_PATH')
        save_path  = os.path.join(image_path, folder)
        save_file  = os.path.join(save_path, row.filename)

        if os.path.exists(save_file):
            return save_file
        else:
            response = requests.get(row.result_image, stream=True)

            if response.status_code == 200:
                mkdirs(save_path)

                with open(save_file, 'wb') as f:
                    for chunk in response.iter_content():
                        f.write(chunk)

                    return save_file
