from os import path
from greenhousemanager import config
import os


def retrieve_failed_uploads():
    failed_uploads = []
    if path.isfile("%s%s" % (config.FAILED_UPLOADS_PATH, config.FAILED_UPLOADS_FILE)):
        failed_uploads_file = open("%s%s" % (config.FAILED_UPLOADS_PATH, config.FAILED_UPLOADS_FILE), 'r+')
        for line in failed_uploads_file:
            failed_uploads.append(eval(line))
        failed_uploads_file.close()
    return failed_uploads


def append_to_failed_uploads(temperature_reading):
    if path.isfile("%s%s" % (config.FAILED_UPLOADS_PATH, config.FAILED_UPLOADS_FILE)):
        failed_uploads_file = open("%s%s" % (config.FAILED_UPLOADS_PATH, config.FAILED_UPLOADS_FILE), 'a')
    else:
        os.makedirs(config.FAILED_UPLOADS_PATH, exist_ok=True)
        failed_uploads_file = open("%s%s" % (config.FAILED_UPLOADS_PATH, config.FAILED_UPLOADS_FILE), 'w+')
    failed_uploads_file.write(str(temperature_reading))
    failed_uploads_file.write('\n')
    failed_uploads_file.close()


def clear_failed_uploads():
    if path.isfile("%s%s" % (config.FAILED_UPLOADS_PATH, config.FAILED_UPLOADS_FILE)):
        failed_uploads_file = open("%s%s" % (config.FAILED_UPLOADS_PATH, config.FAILED_UPLOADS_FILE), 'w+')
        failed_uploads_file.close()


def append_to_log(temperature_reading):
    pass