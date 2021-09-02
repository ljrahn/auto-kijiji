"""
A class to set up logging storing and formatting. loggen method should be called to instantiate a logging session.
Info and errors etc. can then be raised throughout test cases.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from utilities.utils import get_project_root

ROOT_DIR = get_project_root()

class LogGen:
    @staticmethod
    def loggen():
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
        fileHandler = RotatingFileHandler(filename=os.path.join(ROOT_DIR, 'PPT.log'),
                                          maxBytes=10 * 1000 * 1000,
                                          encoding='utf8',
                                          backupCount=5)
        fileHandler.setFormatter(logFormatter)
        rootLogger = logging.getLogger()
        rootLogger.setLevel(logging.INFO)
        rootLogger.addHandler(fileHandler)

        return rootLogger
