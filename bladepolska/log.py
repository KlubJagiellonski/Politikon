import logging
from django.conf import settings

def getlogger():
    logger = logging.getLogger(settings.PROJECT_NAME)
    return logger

def debug(msg):
    logger = getlogger()
    logger.debug(msg)

def info(msg):
    logger = getlogger()
    logger.info(msg)

def error(msg):
    logger = getlogger()
    logger.error(msg)

def warning(msg):
    logger = getlogger()
    logger.warning(msg)

def exception(exc):
    logger = getlogger()
    logger.exception(exc)    