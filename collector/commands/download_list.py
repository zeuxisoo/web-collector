# coding: utf-8

import os
import subprocess
from flask import current_app
from ..models import Stream, Today, TodayDetail
from .base import BaseCommand

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
