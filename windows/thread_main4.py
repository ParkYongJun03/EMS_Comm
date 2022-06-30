# Custom Signal & Slot

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MyApp(QWidget):  # QMainWindow 변경 필요
    closeSignal = pyqtSignal()  # 커스텀 시그널

    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cloese Demo')
        self.resize(300, 300)

        self.btnClose = QPushButton('close', self)
        self.btnClose.clicked.connect(self.btnCloseClicked)
        self.closeSignal.connect(self.onClose)

        self.show()

    def btnCloseClicked(self):
        self.close()

    def onClose(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()
    app.exec_()
