# coding: utf-8

import logging
from flask import current_app
from ..curators import API

class BaseCommand(object):

    def get_curator_api(self):
        return API(current_app.config.get('CURATORS_API_TOKEN'))

    def get_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        logger_stream_handler = logging.StreamHandler()
        logger_stream_handler.setLevel(logging.DEBUG)
        logger_stream_handler.setFormatter(logger_formatter)
        logger.addHandler(logger_stream_handler)

        return logger
