# EMS 대시보드 앱
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import IoT_rc
import requests
import json
import paho.mqtt.client as mqtt  # mqtt subscribe를 위해서 추가
import time
import pymysql
import datetime as dt
from PyQt5.QtChart import QLineSeries, QChart, QDateTimeAxis, QValueAxis

broker_url = '127.0.0.1'  # 로컬에 MQTT Broker가 같이 설치되어 있으므로


class Worker(QThread):
    sigStatus = pyqtSignal(str)  # 연결상태 시그널, 부모클래스 MyApp 전달용
    sigMessage = pyqtSignal(dict)  # MQTT SubSscribe 시그널, MyApp 전달 (dict 중요!)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.host = broker_url
        self.port = 1883
        self.client = mqtt.Client(client_id='Dashboard')

    def onConnect(self, mqtt, obj, flags, rc):
        try:
            print(f'connected with result code > {rc}')
            self.sigStatus.emit('SUCCEED')  # MyApp으로 성공메시지 전달
        except Exception as e:
            print(f'error > {e.args}')
            self.sigStatus.emit('FAILED')

    def onMessage(self, mqtt, obj, msg):
        rcv_msg = str(msg.payload.decode('utf-8'))
        # print(f'{msg.topic} / {rcv_msg}') # 시그널로 전달했ㅇ으므로 주석처리
        self.sigMessage.emit(json.loads(rcv_msg))

        time.sleep(2.0)

    def mqttloop(self):
        self.client.loop()
        print('MQTT client loop')

    def run(self):  # Thread에서는 run() 필수
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.connect(self.host, self.port)
        self.client.subscribe(topic='ems/rasp/data/')
        self.client.loop_forever()


class MyApp(QMainWindow):
    isTempAlarmed = False
    isHumidAlarmed = False
    isTempOn = True
    isHumidOn = True
    tempData = None
    humidData = None
    idx = 0

    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()
        self.showTime()
        self.showWeather()
        self.initThread()
        self.initChart()

    def initChart(self):
        # self. viewLimit = 128  # chart에 그릴 갯수를 제한함
        self.tempData = self.humidData = QLineSeries()
        self.iotChart = QChart()

        # axisX = QDateTimeAxis()
        # axisX.setFormat('HH:mm:ss')
        # axisX.setTickCount(5)
        # dt = QDateTime.currentDateTime()
        # axisX.setRange(dt, dt.addSecs(self.viewLimit))

        # axisY = QValueAxis()

        # self.iotChart.addAxis(axisX, Qt.AlignBottom)
        # self.iotChart.addAxis(axisY, Qt.AlignLeft)
        # self.tempData.attachAxis(axisX)
        # self.humidData.attachAxis(axisX)
        self.iotChart.addSeries(self.tempData)
        self.iotChart.addSeries(self.humidData)
        self.iotChart.layout().setContentsMargins(5, 5, 5, 5)

        self.dataView.setChart(self.iotChart)
        self.dataView.setRenderHints(QPainter.Antialiasing)

        # self.iotData = QLineSeries()
        # self.iotData.append(0, 10)
        # self.iotData.append(1, 20)
        # self.iotData.append(2, 15)
        # self.iotData.append(3, 22)

        # self.iotChart = QChart()
        # self.iotChart.addSeries(self.iotData)
        # self.dataView.setChart(self.iotChart)

    def initThread(self):
        self.myThread = Worker(self)
        self.myThread.sigStatus.connect(self.updateStatus)
        self.myThread.sigMessage.connect(self.updateMessage)
        self.myThread.start()

    @pyqtSlot(dict)
    def updateMessage(self, data):
        # 1. 딕셔너리 분해
        # 2. Label에 Device명칭 업데이트
        # 3. 온도 라벨 현재 온도, 습도 업데이트
        # 4. MySQL DB에 입력
        # 5. 이상온도 알람메시지
        # 6. txbLog 출력
        # 7. Chart에 데이터 추가
        devId = data['DEV_ID']
        print(data)
        self.lblTempTitle.setText(f'{devId} Temperature')
        self.lblHumidTitle.setText(f'{devId} Humidity')
        temp = data['TEMP']  # 3
        humid = data['HUMID']  # 4
        self.lblCurrTemp.setText(f'{temp:.1f}')
        self.lblCurrHumid.setText(f'{humid:.0f}')
        # self.txbLog.append(json.dumps(data))
        self.conn = pymysql.connect(host='127.0.0.1',
                                    user='bms',
                                    password='1234',
                                    db='bms',
                                    charset='euckr')

        # 5.
        if temp >= 30.0:
            self.lblTempAlarm.setText(f'{devId} 이상 기온 감지')
            self.btnTempAlarm.setEnabled(True)  # 버튼 활성화
            self.btnTempStop.setEnabled(True)  # 버튼 비활성화
            if self.isTempAlarmed == False:
                QMessageBox.warning(self, '경고', f'{devId}에서 이상기온감지!!!')
                self.isTempAlarmed = True
        elif temp < 30.0:
            self.lblTempAlarm.setText(f'{devId} 정상기온')
            self.isTempAlarmed = False
            self.btnTempAlarm.setDisabled(True)  # 버튼 활성화
            self.btnTempStop.setDisabled(False)  # 버튼 비활성화

        if humid >= 85.0:
            self.lblTempAlarm.setText(f'{devId} 이상 습도 감지')
            self.btnTempAlarm.setEnabled(True)  # 버튼 활성화
            self.btnTempStop.setEnabled(True)  # 버튼 활성화
            if self.isTempAlarmed == False:
                QMessageBox.warning(self, '경고', f'{devId}에서 이상기온감지!!!')
                self.isTempAlarmed = True
        elif humid <= 85.0:
            self.lblHumidAlarm.setText(f'{devId} 정상습도')
            self.isHumidAlarmed = False
            self.btnHumidAlarm.setDisabled(True)  # 버튼 비활성화
            self.btnHumidStop.setDisabled(False)  # 버튼 비활성화

        # 4. DB입력
        curr_dt = data['CURR_DT']
        query = '''
            INSERT INTO ems_data
                (dev_id, curr_dt, temp, humid)
            VALUES
        		(%s, %s, %s, %s)'''
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, (devId, curr_dt, temp, humid))
                self.conn.commit()
                print('DB Inserted')
        # Chart 업데이트
        self.updateChart(curr_dt, temp, humid)

    def updateChart(self, curr_dt, temp, humid):
        pass
        # self.tempData.append(self.idx, temp)
        # self.humidData.append(self.idx, humid)

        # self.iotChart.

    @pyqtSlot(str)
    def updateStatus(self, stat):
        if stat == 'SUCCEED':
            self.lblStatus.setText('Connected!')
            self.connFrame.setStyleSheet(
                'background-image: url(:/green);'
                'border : none'
            )
        else:
            self.lblStatus.setText('Disconnected!')
            self.connFrame.setStyleSheet(
                'background-image: url(:/red);'
                'border : none'
            )

    def showWeather(self):
        url = 'https://api.openweathermap.org/data/2.5/weather?'\
            'q=seoul&appid=042acd5172a7339f4734ff023897f710'\
            '&lang=kr&units=metric'
        res = requests.get(url)
        res = json.loads(res.text)
        weather = res['weather'][0]['main'].lower()
        self.weatherFrame.setStyleSheet(
            (
                f'background-image: url(:/{weather});'
                'border : none;'
            )
        )
        print(weather)

    def showTime(self):
        today = QDateTime.currentDateTime()
        currDate = today.date()
        currTime = today.time()
        currDay = today.toString('dddd')

        self.lblDate.setText(currDate.toString('yyyy-MM-dd'))
        self.lblDay.setText(currDay)
        self.lblTime.setText(currTime.toString('HH:mm'))
        if today.time().hour() <= 12 and today.time().hour() >= 4:
            self.lblGreeting.setText('Good Morning!')
        elif today.time().hour() <= 18 and today.time().hour() > 12:
            self.lblGreeting.setText('Good Afternoon!')
        elif today.time().hour() <= 24:
            self.lblGreeting.setText('Good Night!')

    def initUI(self):
        uic.loadUi('./ui/dashboard.ui', self)
        self.setWindowIcon(QIcon('./images/iot_64.png'))
        # 화면 정중앙에 위치
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        # 시그널 연결
        self.btnTempAlarm.setDisabled(True)  # 버튼 비활성화
        self.btnTempStop.setEnabled(True)  # 버튼 활성화
        self.btnHumidAlarm.setDisabled(True)  # 버튼 비활성화
        self.btnHumidStop.setEnabled(True)  # 버튼 활성화
        # 위젯 시그널 정의
        self.btnTempAlarm.clicked.connect(self.btnTempAlarmClicked)
        self.btnTempStop.clicked.connect(self.btnTempStopClicked)
        self.btnHumidAlarm.clicked.connect(self.btnHumidAlarmClicked)
        self.btnHumidStop.clicked.connect(self.btnHumidStopClicked)
        self.show()

    def btnTempAlarmClicked(self):
        QMessageBox.information(self, '알람', '이상온도로 에어컨 가동 중')
        self.client = mqtt.Client(client_id='Controller')
        self.client.connect(broker_url, 1883)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID': 'DASHBOARD', 'CURR_DT': curr,
                       'TYPE': 'AIRCON', 'STAT': 'ON'}  # AirCon
        pub_data = json.dumps(origin_data)
        self.client.publish(topic='ems/rasp/control/', payload=pub_data)

    def btnTempStopClicked(self):
        self.client = mqtt.Client(client_id='Controller')
        self.client.connect(broker_url, 1883)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if(self.isTempOn == True):
            QMessageBox.information(self, '정상', '에어컨 중지')
            origin_data = {'DEV_ID': 'DASHBOARD', 'CURR_DT': curr,
                           'TYPE': 'AIRCON', 'STAT': 'OFF'}  # AirCon
            self.insertAlarmData('CONTROL', curr, 'AIRCON', 'OFF')
            self.isTempOn = False
        else:
            QMessageBox.information(self, '정상', '에어컨 실행')
            origin_data = {'DEV_ID': 'DASHBOARD', 'CURR_DT': curr,
                           'TYPE': 'AIRCON', 'STAT': 'ON'}  # AirCon
            self.insertAlarmData('CONTROL', curr, 'AIRCON', 'ON')
            self.isTempOn = True

        pub_data = json.dumps(origin_data)
        self.client.publish(topic='ems/rasp/control/', payload=pub_data)

    def insertAlarmData(self, devId, curr_dt, types, stat):
        self.conn = pymysql.connect(host='127.0.0.1',
                                    user='bms',
                                    password='1234',
                                    db='bms',
                                    charset='euckr')
        query = '''
            INSERT INTO ems_alarm
                (dev_id, curr_dt, type, stat)
            VALUES
        		(%s, %s, %s, %s)'''
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, (devId, curr_dt, types, stat))
                self.conn.commit()
                print('DB Inserted')

    def btnHumidAlarmClicked(self):
        QMessageBox.information(self, '알람', '이상습도로 제습기 가동 중')
        self.client = mqtt.Client(client_id='Controller')
        self.client.connect(broker_url, 1883)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID': 'DASHBOARD', 'CURR_DT': curr,
                       'TYPE': 'DEHUMD', 'STAT': 'ON'}  # DEHUMD
        pub_data = json.dumps(origin_data)
        self.client.publish(topic='ems/rasp/control/', payload=pub_data)
        self.insertAlarmData('CONTROL', curr, 'DEHUMD', 'ON')

    def btnHumidStopClicked(self):
        self.client = mqtt.Client(client_id='Controller')
        self.client.connect(broker_url, 1883)
        curr = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if self.isHumidOn == True:
            QMessageBox.information(self, '정상', '제습기 중지')
            origin_data = {'DEV_ID': 'DASHBOARD', 'CURR_DT': curr,
                           'TYPE': 'DEHUMD', 'STAT': 'OFF'}  # DEHUMD
            self.insertAlarmData('CONTROL', curr, 'DEHUMD', 'OFF')
            self.isHumidOn = False
        else:
            QMessageBox.information(self, '정상', '제습기 실행')
            origin_data = {'DEV_ID': 'DASHBOARD', 'CURR_DT': curr,
                           'TYPE': 'DEHUMD', 'STAT': 'ON'}  # DEHUMD
            self.insertAlarmData('CONTROL', curr, 'DEHUMD', 'ON')
            self.isHumidOn = True
        pub_data = json.dumps(origin_data)
        self.client.publish(topic='ems/rasp/control/', payload=pub_data)

    # 종료 메시지박스

    def closeEvent(self, signal):
        ans = QMessageBox.question(
            self, '종료', '종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            self.conn.close()  # DB 접속 끊기
            signal.accept()
        else:
            signal.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()
