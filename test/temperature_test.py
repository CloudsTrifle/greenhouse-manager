import unittest

import mock
from elasticsearch import Elasticsearch

import temperatures_handler
from src import archived_data_helper
from src.thermometer import Thermometer


class TestTemperatureReadings(unittest.TestCase):

    def tearDown(self):
        archived_data_helper.clear_failed_uploads()

    @mock.patch.object(Thermometer, 'current_temperature')
    @mock.patch.object(Elasticsearch, 'index')
    def test_thermometer_handler_happy_path(self, mock_es, mock_temperature):
        mock_temperature.return_value = 10.6
        temperatures_handler.main()
        mock_es.assert_called_with(body={'temp_greenhouse': 10.6,
                                         '@timestamp': mock.ANY,
                                         'temp_outside': 10.6,
                                         'ts': mock.ANY},
                                   doc_type='temperature_readings', id=mock.ANY, index='temperatures')

    @mock.patch.object(Thermometer, 'current_temperature')
    @mock.patch.object(Elasticsearch, 'index')
    def test_thermometer_handler_failed_uploads(self, mock_es, mock_temperature):
        mock_temperature.return_value = 10.6
        mock_es.side_effect = Exception()
        temperatures_handler.main()
        temperatures_handler.main()
        temperatures_handler.main()

        failed_uploads = archived_data_helper.retrieve_failed_uploads()
        assert(len(failed_uploads) == 3)

    @mock.patch.object(Thermometer, 'current_temperature')
    @mock.patch.object(Elasticsearch, 'index')
    def test_thermometer_handler_failed_then_successful_uploads(self, mock_es, mock_temperature):
        mock_temperature.return_value = 10.6

        first_fail = {'@timestamp': '2017-03-06T10:00:00',
                      'temp_greenhouse': 5.5,
                      'temp_outside': 6.5,
                      'ts': 12345
                      }
        second_fail = {'@timestamp': '2017-03-06T11:00:00',
                       'temp_greenhouse': 7.5,
                       'temp_outside': 8.5,
                       'ts': 67890
                       }

        archived_data_helper.append_to_failed_uploads(first_fail)
        archived_data_helper.append_to_failed_uploads(second_fail)

        temperatures_handler.main()

        assert 3 == mock_es.call_count

    def test_no_failed_uploads(self):
        failed_uploads = archived_data_helper.retrieve_failed_uploads()
        assert (len(failed_uploads) == 0)


if __name__ == '__main__':
    unittest.main()
