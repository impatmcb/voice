import speech_recognition as sr
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
from whoosh import qparser
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QSize, QCoreApplication
from PyQt5.QtGui import QIcon
import textwrap
import webbrowser
from urllib.parse import urlencode

sample_rate = 48000
chunk_size = 2048
r = sr.Recognizer()
device_id = 1
convertedtext = {}


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(550, 250, 512, 768)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle("SutterVoice - SHIS Service Desk")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.__press_pos = None
        self.initUI()

    def initUI(self):
        self.background = QtWidgets.QLabel(self)
        self.background.setStyleSheet("background-image: url(UI.png);")
        self.background.setGeometry(0, 0, 512, 768)

        self.label = QtWidgets.QLabel(self)
        self.label.setText("")
        self.label.setGeometry(50, 100, 360, 90)
        self.label.setStyleSheet("font-size: 9pt;"
                                 "color: rgb(80, 127, 112);"
                                 "font-family: 'Arial Black', Gadget, sans-serif;")

        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText("")
        self.label1.setGeometry(50, 200, 360, 90)
        self.label1.setStyleSheet("font-size: 9pt;"
                                  "color: rgb(80, 127, 112);"
                                  "font-family: 'Arial Black', Gadget, sans-serif;")

        self.label2 = QtWidgets.QLabel(self)
        self.label2.setText("")
        self.label2.setGeometry(50, 300, 360, 90)
        self.label2.setStyleSheet("font-size: 9pt;"
                                  "color: rgb(80, 127, 112);"
                                  "font-family: 'Arial Black', Gadget, sans-serif;")

        self.label3 = QtWidgets.QLabel(self)
        self.label3.setText("")
        self.label3.setGeometry(50, 400, 360, 90)
        self.label3.setStyleSheet("font-size: 9pt;"
                                  "color: rgb(80, 127, 112);"
                                  "font-family: 'Arial Black', Gadget, sans-serif;")

        self.label4 = QtWidgets.QLabel(self)
        self.label4.setText("")
        self.label4.setGeometry(50, 500, 360, 90)
        self.label4.setStyleSheet("font-size: 9pt;"
                                  "color: rgb(80, 127, 112);"
                                  "font-family: 'Arial Black', Gadget, sans-serif;")

        self.linklabel = QtWidgets.QPushButton(self)
        self.linklabel.setIcon(QIcon('/SutterVoice/right.png'))
        self.linklabel.setGeometry(426, 130, 34, 34)
        self.linklabel.hide()

        self.linklabel1 = QtWidgets.QPushButton(self)
        self.linklabel1.setIcon(QIcon('/SutterVoice/right.png'))
        self.linklabel1.setGeometry(426, 230, 34, 34)
        self.linklabel1.hide()

        self.linklabel2 = QtWidgets.QPushButton(self)
        self.linklabel2.setIcon(QIcon('/SutterVoice/right.png'))
        self.linklabel2.setGeometry(426, 330, 34, 34)
        self.linklabel2.hide()

        self.linklabel3 = QtWidgets.QPushButton(self)
        self.linklabel3.setIcon(QIcon('/SutterVoice/right.png'))
        self.linklabel3.setGeometry(426, 430, 34, 34)
        self.linklabel3.hide()

        self.linklabel4 = QtWidgets.QPushButton(self)
        self.linklabel4.setIcon(QIcon('/SutterVoice/right.png'))
        self.linklabel4.setGeometry(426, 530, 34, 34)
        self.linklabel4.hide()

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("")
        self.b1.clicked.connect(self.clicked)
        self.b1.setStyleSheet("background-color: rgba(255,255,255,0);")
        self.b1.setGeometry(192, 634, 128, 110)

        self.close = QtWidgets.QPushButton(self)
        self.close.setText("")
        self.close.clicked.connect(QCoreApplication.instance().quit)
        self.close.setStyleSheet("background-color: rgba(255,255,255,0);")
        self.close.setGeometry(480, 20, 24, 24)

        self.line = QtWidgets.QLabel(self)
        self.line.setStyleSheet("background-image: url(hline.png);")
        self.line.setGeometry(56, 190, 400, 10)
        self.line.hide()

        self.line1 = QtWidgets.QLabel(self)
        self.line1.setStyleSheet("background-image: url(hline.png);")
        self.line1.setGeometry(56, 290, 400, 10)
        self.line1.hide()

        self.line2 = QtWidgets.QLabel(self)
        self.line2.setStyleSheet("background-image: url(hline.png);")
        self.line2.setGeometry(56, 390, 400, 10)
        self.line2.hide()

        self.line3 = QtWidgets.QLabel(self)
        self.line3.setStyleSheet("background-image: url(hline.png);")
        self.line3.setGeometry(56, 490, 400, 10)
        self.line3.hide()

        self.move(QApplication.instance().desktop().screen().rect().center()
                  - self.rect().center())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.__press_pos = event.pos()  # remember starting position

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.__press_pos = None

    def mouseMoveEvent(self, event):
        if self.__press_pos:  # follow the mouse
            self.move(self.pos() + (event.pos() - self.__press_pos))

    def clicked(self):
        try:
            with sr.Microphone(device_index=device_id, sample_rate=sample_rate, chunk_size=chunk_size) as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)

                text = r.recognize_google(audio)
                ix = open_dir("/SutterVoice/indexdir")

                topN = 5
                searcher = ix.searcher(weighting=scoring.BM25F)
                parser = QueryParser("content", ix.schema, group=qparser.OrGroup).parse(text)

                results = searcher.search(parser, limit=topN)
                convertedtext += split(text, " ")

                x = 1
                for res in results:
                    if x == 1:
                        lab = textwrap.fill(res['title'], 39)
                        search = {'rectype': 'KCS Article', 'search': res['title']}
                        global labtt
                        labtt = urlencode(search)
                    elif x == 2:
                        lab1 = textwrap.fill(res['title'], 39)
                        search = {'rectype': 'KCS Article', 'search': res['title']}
                        global labtt1
                        labtt1 = urlencode(search)
                    elif x == 3:
                        lab2 = textwrap.fill(res['title'], 39)
                        search = {'rectype': 'KCS Article', 'search': res['title']}
                        global labtt2
                        labtt2 = urlencode(search)
                    elif x == 4:
                        lab3 = textwrap.fill(res['title'], 39)
                        search = {'rectype': 'KCS Article', 'search': res['title']}
                        global labtt3
                        labtt3 = urlencode(search)
                    elif x == 5:
                        lab4 = textwrap.fill(res['title'], 39)
                        search = {'rectype': 'KCS Article', 'search': res['title']}
                        global labtt4
                        labtt4 = urlencode(search)

                    x += 1
                searcher.close()
                print()

        except sr.UnknownValueError:
            print("I couldn't understand you, try again.")

        except sr.RequestError as e:
            print(f"Could not request results from Google. {e}")

        self.label.setText(lab)
        self.label1.setText(lab1)
        self.label2.setText(lab2)
        self.label3.setText(lab3)
        self.label4.setText(lab4)
        self.linklabel.show()
        self.linklabel1.show()
        self.linklabel2.show()
        self.linklabel3.show()
        self.linklabel4.show()
        self.line.show()
        self.line1.show()
        self.line2.show()
        self.line3.show()
        self.linklabel.clicked.connect(self.clickedurl)
        self.linklabel1.clicked.connect(self.clickedurl1)
        self.linklabel2.clicked.connect(self.clickedurl2)
        self.linklabel3.clicked.connect(self.clickedurl3)
        self.linklabel4.clicked.connect(self.clickedurl4)

    def clickedurl(self):
        webbrowser.open("cherwellclient://commands/search?" + labtt)

    def clickedurl1(self):
        webbrowser.open("cherwellclient://commands/search?" + labtt1)

    def clickedurl2(self):
        webbrowser.open("cherwellclient://commands/search?" + labtt2)

    def clickedurl3(self):
        webbrowser.open("cherwellclient://commands/search?" + labtt3)

    def clickedurl4(self):
        webbrowser.open("cherwellclient://commands/search?" + labtt4)


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


window()
