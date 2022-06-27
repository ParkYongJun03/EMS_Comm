# PYQT 학습
from PyQt5 import QtWidgets


def run():
    app = QtWidgets.QApplication([])  # App 객체 생성
    wnd = QtWidgets.QMainWindow()   # window 객체 생성
    label = QtWidgets.QLabel('\tQt 안녕! QT')  # 라벨 위젯 생성
    wnd.setCentralWidget(label)     # 윈도우 정중앙 위치
    wnd.show()
    app.exec_()


if __name__ == '__main__':
    run()
