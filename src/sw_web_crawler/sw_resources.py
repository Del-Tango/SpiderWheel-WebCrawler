import time
import logging
import pysnooper

from os import path, makedirs


# LOGGING


#@pysnooper.snoop()
def log_init(file_path, log_format, timestamp_format, log_name=__name__):
    log = logging.getLogger(log_name)
    try:
        log.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(file_path, 'a')
        formatter = logging.Formatter(log_format, timestamp_format)
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
    finally:
        return log


# ENSURANCE


def ensure_files_exist(*args):
    for file_path in args:
        with open(file_path, 'w', encoding='utf-8', errors='ignore'):
            pass
    return True


def ensure_directories_exist(*args):
    for dir_path in args:
        try:
            makedirs(dir_path)
        except OSError as e:
            pass


# GETTERS


def get_time():
    return time.strftime('%H:%M:%S')


def get_full_time():
    return time.strftime('%H:%M:%S, %A %b %Y')
