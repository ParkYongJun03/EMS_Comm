import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import RPi.GPIO as GPIO
import time

SB = 15
GPIO.setmode(GPIO.BOARD)  # GOIO.BOARD
GPIO.setup(SB, GPIO.OUT)  # 15핀 할당

pwm = GPIO.PWM(SB, 50)  # 50Hz
pwm.start(3.0)  # 0.6ms


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('RPi SURVO Control')
        # 윈도우 기본설정
        self.setGeometry(100, 100, 300, 350)  # ax, ay, aw, ah

        self.label = QLabel(self)
        self.label.setFont(QFont('Arial', 15))
        self.label.setText('SURVO MOTOR Control')
        self.label.setAlignment(Qt.AlignCenter)  # 라벨 정중앙

        # 다이얼
        self.dial = QDial(self)
        self.dial.setRange(0, 13)

        # 시그널
        self.dial.valueChanged.connect(self.Dial_Changed)

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.dial)
        self.vbox.addWidget(self.label)
        self.show()

    def Dial_Changed(self):
        self.label.setText(str(self.dial.value()))
        pwm.ChangeDutyCycle(float(self.dial.value()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MyApp()
    app.exec()
# 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
