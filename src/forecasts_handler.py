import requests
from elasticsearch import Elasticsearch
import time

apiKey = "c84daf387b748d448d3f367600e2950c"
location = "holytown"

r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q=%s&APPID=%s' % (location, apiKey))
results = r.json()

es = Elasticsearch([{'host': '192.168.0.12', 'port': 9200}])

for result in results['list']:
    temp =  result['main']['temp']
    dateTime =  result['dt_txt']
    weatherDescription = result['weather'][0]['description']

    tempInCelsius = float(temp) - 273.15
    timestamp = dateTime.replace(' ', 'T')

    ts = time.time()
    es.index(index='forecasts', doc_type='forecast', id=ts, body={'@timestamp': timestamp, 'temp': tempInCelsius, 'description': weatherDescription})