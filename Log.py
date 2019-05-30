__author__ = 'Dengbo'

import logging


class Log:

    logging = {}
    filename = "rtsp.log"

    def __init__(self):
        self.logging = logging
        self.logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S', filename=self.filename, filemode='a')

    def GetLogging(self):

        return self.logging