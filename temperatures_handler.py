print("Executing Thermometer Readings")

import time
import datetime

print("config")
import src.config as config

print("archive")
import src.archived_data_helper as archived_data_handler

print("elastic")
from elasticsearch import Elasticsearch

print("thermometer")
from src.thermometer import Thermometer


def main():
    greenhouse_thermometer = Thermometer(config.GREENHOUSE_THERMOMETER_ID)
    outside_thermometer = Thermometer(config.OUTSIDE_THERMOMETER_ID)

    greenhouse_temperature = greenhouse_thermometer.current_temperature()
    outside_temperature = outside_thermometer.current_temperature()

    es = Elasticsearch([{'host': config.ELASTICSEARCH_HOST, 'port': config.ELASTICSEARCH_PORT}])

    ts = time.time()
    datetime_string = datetime.datetime.fromtimestamp(ts).strftime(config.ELASTICSEARCH_TIMESTAMP_FORMAT)

    current_reading = {'@timestamp': datetime_string,
                       'temp_greenhouse':greenhouse_temperature,
                       'temp_outside':outside_temperature,
                       'ts': ts
                       }

    data_to_upload = archived_data_handler.retrieve_failed_uploads()
    data_to_upload.append(current_reading)

    try:
        for data in data_to_upload:
            es.index(
                index='temperatures',
                doc_type='temperature_readings',
                id=data['ts'],
                body=data
                )

        archived_data_handler.clear_failed_uploads()
        archived_data_handler.append_to_log(current_reading)

    except Exception as e:
        archived_data_handler.append_to_failed_uploads(current_reading)
        if len(data_to_upload) > 11:
            #restart
            pass
        pass