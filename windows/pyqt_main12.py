# 네이버 검색용 UI 실행

import json
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from json import *  # 검색결과를 json 타입으로 받음
import urllib.request  # URL openAPI 검색 위해 필요
from urllib.parse import quote
import webbrowser  # 웹브라우저 열기 위한 패키지


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./ui/네이버뉴스 검색.ui', self)
        self.setWindowIcon(QIcon('./images/navericon.png'))

        # 시그널 연결

        self.btnSearch.clicked.connect(self.btnSearchClicked)
        self.txtSearch.returnPressed.connect(self.btnSearchClicked)
        self.tblResult.itemSelectionChanged.connect(self.tblResultSelected)
        self.show()

    def tblResultSelected(self):
        selected = self.tblResult.currentRow()  # 현재 선택된 열의 인덱스
        url = self.tblResult.item(selected, 1).text()
        webbrowser.open(url)

    def btnSearchClicked(self):
        #        QMessageBox.show(self)
        print('검색시작')
        jsonResult = []
        totalResult = []
        keyword = 'news'
        search_word = self.txtSearch.text()
        display_count = 50

        jsonResult = self.getNaverSearch(
            keyword, search_word, 1, display_count)
        # print(jsonResult)

#        while jsonResult != None and jsonResult['display'] != 0:
        for post in jsonResult['items']:
            totalResult.append(self.getPostData(post))

        self.makeTable(totalResult)
        # list view 봉인
        # model = QStandardItemModel()
        # self.lsvResult.setModel(model)

        # for i in totalResult:
        #     item = QStandardItem(i[0]['title'])
        #     model.appendRow(item)
    def makeTable(self, result):
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblResult.setColumnCount(2)
        self.tblResult.setRowCount(len(result))  # 50
        self.tblResult.setHorizontalHeaderLabels(['기사제목', '뉴스링크'])
        self.tblResult.setColumnWidth(0, 350)
        self.tblResult.setColumnWidth(1, 300)
        self.tblResult.setEditTriggers(
            QAbstractItemView.NoEditTriggers)  # read only

        # 테이블 위젯 설정

        i = 0
        for item in result:  # 50번 반복
            title = self.strip_tag(item[0]['title'])
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(item[0]['org_link']))
            i += 1

    def strip_tag(self, title):
        ret = title.replace('&lt;', '<')
        ret = ret.replace('&gt', '>')
        ret = ret.replace('&quot', '"')
        ret = ret.replace('<b>', '')
        ret = ret.replace('</b>', '')
        ret = ret.replace(';', '')
        return ret
    # 핵심 함수

    def getNaverSearch(self, keyword, search_word, start_count, dispaly_count):
        url = f'https://openapi.naver.com/v1/search/{keyword}.json' \
            f'?query={quote(search_word)}&start={start_count}&display={dispaly_count}'

        req = urllib.request.Request(url)
        # 인증추가
        req.add_header('X-Naver-Client-Id', 'tvedvKs3IPxZVukY2DH9')
        req.add_header('X-Naver-Client-Secret', 'pTBI2SycI5')

        res = urllib.request.urlopen(req)  # request에 대한 response
        if res.getcode() == 200:
            print('URL request success')
        else:
            print('URL request failed')
        ret = res.read().decode('utf-8')
        if ret == None:
            return None
        else:
            return json.loads(ret)

    def getPostData(self, post):
        temp = []
        title = post['title']
        description = post['description']
        org_link = post['originallink']
        link = post['link']

        temp.append({'title': title, 'description': description,
                     'org_link': org_link, 'link': link})
        return temp


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyApp()

    app.exec_()
