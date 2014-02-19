# coding: utf-8

import os
import errno
import requests
from flask import current_app
from ..models import Stream

def mkdirs(directory):
    try:
        os.makedirs(directory)
    except OSError as err:
        if err.errno == errno.EEXIST and os.path.isdir(directory):
            pass

def download_image(result_id):
    stream = Stream.query.filter_by(result_id=result_id).first()

    if stream:
        image_path = current_app.config.get('IMAGE_DOWNLOAD_PATH')
        save_path  = os.path.join(image_path, 'stream')
        save_file  = os.path.join(save_path, stream.filename)

        if os.path.exists(save_file):
            return save_file
        else:
            response = requests.get(stream.result_image, stream=True)

            if response.status_code == 200:
                mkdirs(save_path)

                with open(save_file, 'wb') as f:
                    for chunk in response.iter_content():
                        f.write(chunk)

                    return save_file
