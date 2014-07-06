# coding: utf-8

import os
from flask import current_app
from ..models import Stream, Today, TodayDetail
from .base import BaseCommand

class EchoList(BaseCommand):

    def __init__(self, table=None):
        self.logger = self.get_logger()
        self.table  = table

    def make(self):
        if self.table is None:
            self.logger.error('Please enter table name')
        else:
            self.logger.info("EchoList")
            self.logger.info("==> table: {0}".format(self.table))

            file_path     = os.path.join(current_app.static_folder, 'echolist.{0}.txt'.format(self.table))
            target_models = {
                'stream'     : Stream,
                'today'      : Today,
                'todaydetail': TodayDetail
            }

            with open(file_path, 'w+') as f:
                for row in target_models[self.table].query.all():
                    self.logger.info("==> saving {0}".format(row.result_image))
                    f.write(row.result_image + "\n")
                f.close()

            self.logger.info("saved to {0}".format(file_path))
