# coding: utf-8

import os
import subprocess
from flask import current_app
from ..models import db, Stream, Today, TodayDetail
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

class DownloadList(BaseCommand):

    def __init__(self, table=None):
        self.logger = self.get_logger()
        self.table  = table

    def make(self, show_aria2c=False):
        self.logger.info("DownloadList")

        if self.table is None:
            self.logger.error('Please enter table name')
        else:
            list_file_path = os.path.join(current_app.static_folder, 'echolist.{0}.txt'.format(self.table))

            if not os.path.exists(list_file_path):
                self.logger.error("Not found the echolist in {0}".format(list_file_path))
                self.logger.error("Please ran command to generate the list file: python manager.py echolist")
            else:
                save_dir = os.path.join(current_app.config.get('IMAGE_DOWNLOAD_PATH'), 'aria2c/{0}'.format(self.table))
                command  = "aria2c -i {0} -d {1}".format(list_file_path, save_dir)

                self.logger.info("==> list: {0}".format(list_file_path))
                self.logger.info("==> running command")
                self.logger.info("==> {0}".format(command))

                try:
                    if show_aria2c:
                        subprocess.call(command, shell=True)
                    else:
                        process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        stdout, stderr = process.communicate()
                except KeyboardInterrupt:
                    self.logger.info("==> command stopped by entered ctrl+c")

                self.logger.info("==> all url saved to {0}".format(save_dir))

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
