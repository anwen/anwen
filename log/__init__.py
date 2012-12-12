# -*- coding: utf-8 -*-
import logging
import options
import tornado.options
from logging.handlers import RotatingFileHandler

tornado.options.enable_pretty_logging()


for logger_name, path in options.log['log_path'].iteritems():
    name = logger_name if logger_name != 'logger' else None
    logger = locals()[logger_name] = logging.getLogger(name)
    logger.setLevel(logging.NOTSET)
    file_handler = RotatingFileHandler(
        path,
        maxBytes=options.log['log_max_bytes'],
        backupCount=options.log['backup_count']
    )
    file_handler.setFormatter(tornado.options._LogFormatter(color=False))
    logger.addHandler(file_handler)
