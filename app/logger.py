import logging
import os
from pythonjsonlogger import jsonlogger

import config

config = config.config()

def getLogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(os.getenv('WEBMON_LOG_LEVEL', config.logging.level))
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(fmt='%(asctime)s %(levelname)s %(thread)s %(threadName)s %(module)s %(message)s')
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    return logger