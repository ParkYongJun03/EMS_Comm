# LED Control UI

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import RPi.GPIO as GPIO
import time

BUTTON = 3
RED = 11

GPIO.setmode(GPIO.BOARD) # GOIO.BCM
GPIO.setup(RED, GPIO.OUT) # 11핀 출력 세팅
GPIO.setup(BUTTON, GPIO.IN)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def btnOn_Clicked(self):
        GPIO.output(RED, 1)
        self.label.setText('LED ON!')

    def btnOff_Clicked(self):
        GPIO.output(RED, 0)
        self.label.setText('LED OFF!')
    def closeEvent(self, QCloseEvent) : 
        GPIO.output(RED, GPIO.LOW)
        GPIO.cleanup()

        self.deleteLater()
        QCloseEvent.accept()
    def initUI(self):
        self.setWindowTitle('RPi LED Control')
        # 윈도우 기본설정
        self.setGeometry(100, 100, 300, 350)  # ax, ay, aw, ah

        self.label = QLabel(self)
        self.label.setFont(QFont('Arial', 15))
        self.label.setText('LE Control')
        self.label.setAlignment(Qt.AlignCenter)  # 라벨 정중앙

        self.btnOn = QPushButton('LED ON', self)
        self.btnOff = QPushButton('LED Off', self)

        # 시그널
        self.btnOn.clicked.connect(self.btnOn_Clicked)
        self.btnOff.clicked.connect(self.btnOff_Clicked)

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.label)

        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.btnOn)
        self.hbox.addWidget(self.btnOff)

        self.vbox.addLayout(self.hbox)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()
    app.exec()
<<<<<<< HEAD
# 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
=======
    # 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
>>>>>>> 74db1c145f824e2d96b2ae1d58f4024c16296c6e
