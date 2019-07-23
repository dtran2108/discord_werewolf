from colorlog import ColoredFormatter
import logging


def get_logger():
    LOG_LEVEL = logging.DEBUG
    LOGFORMAT = '%(asctime)s \033[1m%(log_color)s%(levelname)s%(reset)s\033[0m %(filename)s %(funcName)s:%(lineno)d %(message)s'
    logging.root.setLevel(LOG_LEVEL)
    formatter = ColoredFormatter(LOGFORMAT)
    stream = logging.StreamHandler()
    stream.setLevel(LOG_LEVEL)
    stream.setFormatter(formatter)
    log = logging.getLogger('pythonConfig')
    return log, LOG_LEVEL, stream
