# LED Control UI

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def btnOn_Clicked(self):
        self.label.setText('LED ON!')

    def btnOff_Clicked(self):
        self.label.setText('LED OFF!')

    def initUI(self):
        self.setWindowTitle('RPi LED Control')
        # 윈도우 기본설정
        self.setGeometry(100, 100, 300, 350)  # ax, ay, aw, ah

        self.label = QLabel(self)
        self.label.setFont(QFont('Arial', 15))
        self.label.setText('LED Control')
        self.label.setAlignment(Qt.AlignCenter)  # 라벨 정중앙

        self.btnOn = QPushButton('LED ON', self)
        self.btnOff = QPushButton('LED Off', self)

        # 시그널 정의
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
    # 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
