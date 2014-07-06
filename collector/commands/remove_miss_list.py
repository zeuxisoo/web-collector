# coding: utf-8

import os
from flask import current_app
from ..models import db, Stream, Today, TodayDetail
from .base import BaseCommand

class RemoveMissList(BaseCommand):

    def __init__(self, table=None):
        self.logger = self.get_logger()
        self.table  = table

    def make(self):
        if self.table is None:
            self.logger.error('Please enter table name')
        else:
            self.logger.info("RemoveMissList")
            self.logger.info("==> table: {0}".format(self.table))

            # Model mapping
            target_models = {
                'stream'     : Stream,
                'today'      : Today,
                'todaydetail': TodayDetail
            }
            target_model  = target_models[self.table]

            # Find missed record
            target_folder = os.path.join(current_app.config.get('IMAGE_DOWNLOAD_PATH'), 'aria2c/{0}'.format(self.table))
            missed_count  = 0
            missed_ids    = []

            for row in target_model.query.all():
                saved_file_path = os.path.join(target_folder, os.path.basename(row.result_image))

                if not os.path.exists(saved_file_path):
                    self.logger.info("==> missed: {0}".format(row.result_image))

                    missed_count = missed_count + 1
                    missed_ids.append(row.id)

            self.logger.info("==> running delete")

            # Delete missed record
            # - In SQLAlchemy session, the delete doesn't hit the database until a commit, so there's no problem
            deleted_count = 0
            for missed_id in missed_ids:
                row = db.session.query(target_model).get(missed_id)
                row.delete()

                self.logger.info("--> deleted: {0}".format(row.result_image))

                deleted_count = deleted_count + 1

            db.session.commit()

            #
            self.logger.info("==> missed: {0} deleted: {1}".format(missed_count, deleted_count))
