# MQTT Pub/Sub App
from threading import Thread, Timer
import paho.mqtt.client as mqtt
import time
import datetime as dt
import json
import adafruit_dht as dht
import board
# DHT 센서 값 Publish
SENSOR = dht.DHT11(board.D2)


class publisher(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.host = '192.168.0.21'  # 내서버
        self.port = 1883
        print('publisher 스레드 시작')
        self.client = mqtt.Client(client_id='EMS105')

    def run(self):
        self.client.connect(self.host, self.port)
        self.publishDataAuto()

    def publishDataAuto(self):
        t = SENSOR.temperature
        h = SENSOR.humidity
        try:
            curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            originData = {'DEV_ID': 'EMS05', 'CURR_DT': curr,
                          'TEMP': t, 'HUMID': h}
            pubData = json.dumps(originData)

            self.client.publish(topic='ems/rasp/control/', payload=pubData)
            print(f'{curr} -> MQTT published')
            Timer(2.0, self.publishDataAuto).start()

        except RuntimeError as e:
            print(f'ERROR > {e.args[0]}')


class subscriber(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.host = '192.168.0.21'  # 내서버
        self.port = 1883
        print('subscriber 스레드 시작')
        self.client = mqtt.Client(client_id='EMS005')

    def onConnect(self, mqttc, obj, flags, rc):
        print(f'sub : connected with rc > {rc}')

    def onMessage(self, mqttc, obj, msg):
        rcv_msg = str(msg.payload.decode('utf-8'))
        print(f'{msg.topic} / {rcv_msg}')
        time.sleep(1.0)

    def run(self):
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.connect(self.host, self.port)
        self.client.subscribe(topic='ems/rasp/control/')
        self.client.loop_forever()


if __name__ == '__main__':
    thPub = publisher()
    thPub.start()
    thSub = subscriber()
    thSub.start()
