# 동시에 두가지 태스크
# from multiprocessing import parent_process
from threading import Thread, Timer
import paho.mqtt.client as mqtt
import time
import datetime as dt
import json


class publisher(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.host = '127.0.0.1'
        self.port = 1883
        print('publisher 스레드 시작')
        self.client = mqtt.Client(client_id='EMS101')

    def run(self):
        self.client.connect(self.host, self.port)
        self.publishDataAuto()

    def publishDataAuto(self):
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        originData = {'DEV_ID': 'DASHBOARD', 'CURR_DT': curr,
                      'TYPE': 'DEHUMD', 'STAT': 'ON'}  # AirCon
        pubData = json.dumps(originData)

        self.client.publish(topic='ems/rasp/control/', payload=pubData)
        print('Published')

        Timer(3.0, self.publishDataAuto).start()


class subscriber(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.host = '127.0.0.1'  # 추후 변경
        self.port = 1883
        print('subscriber 스레드 시작')
        self.client = mqtt.Client(client_id='EMS001')

    def onConnect(self, mqttc, obj, flags, rc):
        print(f'sub : connected with rc > {rc}')

    def onMessage(self, mqttc, obj, msg):
        rcv_msg = str(msg.payload.decode('utf-8'))
        print(f'{msg.topic} / {rcv_msg}')
        time.sleep(2.0)

    def run(self):
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.connect(self.host, self.port)
        self.client.subscribe(topic='ems/rasp/data/')
        self.client.loop_forever()


if __name__ == '__main__':
    thPub = publisher()
    thPub.start()
    thSub = subscriber()
    thSub.start()
