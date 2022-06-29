# EMS 대시보드 앱
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./ui/dashboard.ui', self)
        self.setWindowIcon(QIcon('./images/automation.png'))

        # 시그널 연결

        # self.btnSearch.clicked.connect(self.btnSearchClicked)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()

    app.exec_()
