# EMS 대시보드 앱
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import IoT_rc

import requests
import json


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()
        self.showTime()
        self.showWeather()

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

        # 시그널 연결

        # self.btnSearch.clicked.connect(self.btnSearchClicked)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()
