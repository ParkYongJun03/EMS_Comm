# MQTT Publisher
# sudo pip install aho-mqtt
import threading
import datetime as dt
import paho.mqtt.client as mqtt
import json
import adafruit_dht as dht
import time
import board

SENSOR = dht.DHT11(board.D2)

client2 = None
count = 0

def publish_sensor_data():
    try:
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        t= SENSOR.temperature
        h= SENSOR.humidity
        origin_data = {'DEV_ID' : 'EMS05', 'CURR_DT' : curr,
            'TEMP' : t, 'HUMID' : h}
        pub_data = json.dumps(origin_data)
        client2.publish(topic='ems/rasp/data/', payload=pub_data)

        print(f'{curr} -> MQTT published')
        print(f'TEMP > {t:.1f}`C / HUMID > {h:.1f}%')
    except RuntimeError as e:
        print(f'ERROR > {e.args[0]}')

    threading.Timer(2.0, publish_sensor_data).start()

if __name__ == '__main__':
    broker_url = '192.168.0.21'
    client2 = mqtt.Client(client_id='EMS05')
    client2.connect(host=broker_url, port=1883)

    publish_sensor_data()