import mock
import unittest
from elasticsearch import Elasticsearch
from greenhousemanager import temperatures_handler

from greenhousemanager.thermometer import Thermometer

class TestTemperatureReadings(unittest.TestCase):

    @mock.patch.object(Thermometer, 'current_temperature')
    @mock.patch.object(Elasticsearch, 'index')
    def test_thermometer_handler_happy_path(self, mock_es, mock_temperature):
        mock_temperature.return_value = 10.6
        temperatures_handler.main()
        mock_es.assert_called_with(body={'temp_greenhouse': 10.6, '@timestamp': mock.ANY, 'temp_outside': 10.6}, doc_type='temperature_readings', id=mock.ANY, index='temperatures')

if __name__ == '__main__':
    unittest.main()
