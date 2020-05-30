# -*- coding: utf-8 -*-
import os
import logging


def get_logger(file_name, log_name, log_level=logging.DEBUG):
    dir_name = os.path.dirname(file_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s| %(message)s')
    log = logging.getLogger(name=log_name)
    if len(log.handlers):
        return log
    handler = logging.FileHandler(file_name)
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(log_level)
    return log


from core.core_metric import metrics_registry
from core.custom_metric import m_instance

__all__ = [
    "get_logger",
    "metrics_registry",
    "m_instance"
]