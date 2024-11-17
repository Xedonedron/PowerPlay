from kafka import KafkaProducer
from datetime import date
import time
import time
import requests
import json

producer = KafkaProducer(
    bootstrap_servers = ['localhost:9092'],
    key_serializer = lambda k:str(k).encode('utf-8'),
    value_serializer = lambda v: json.dumps(v).encode('utf-8')
)

today = date.today()

def hit_api(object):
    url = f'http://172.104.52.184:6717/api/node_1/{object}/from={today}'
    response = requests.get(url)
    raw = response.json()
    timestamp = raw[-1]['x']
    return raw, timestamp

if __name__ == '__main__':
    iot_objects = ['soil_ph', 'temperature', 'battery', 'potassium']
    last_data = {}

    while True: 
        for object in iot_objects:
            raw_data, timestamp_check = hit_api(object)

            # if timestamp_check not in last_data:
            if object not in last_data:
                sensor_value = raw_data[-1]['y']
            
                producer.send(
                    'iot_sensors',
                    key=object,
                    value=raw_data # kirim response.json()
                )

                print(f'Get {object} with value -> {sensor_value}')

                last_data[object] = timestamp_check
            
            else:
                print("Fetched data still same")
            time.sleep(3)