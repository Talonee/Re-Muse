from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from clean import GetJson
from search import Search

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


import os, shutil, unidecode, time, json, urllib.request, sys

class ReMuse(QThread):
    countChanged = pyqtSignal(int) # must remain outside of init

    def __init__(self, songs):
        QThread.__init__(self)
        self.songs = songs
        self.length = len(self.songs)
             
    def run(self):
        self.options = Options()
        # self.options.add_argument("headless")
        self.options.add_argument("--incognito")
        self.options.add_argument("--mute-audio")
        self.driver = webdriver.Chrome(executable_path='chromedriver', options=self.options)
        self.driver.get("https://music.youtube.com/")
        self.driver.execute_script("window.open('http://www.google.com/');")
        for song in self.songs:
            mehoy = unidecode.unidecode(song["File"])
            print(f"Starting {mehoy}")
            Search(self.driver, song).find()
            print(f"Finished with {mehoy}")
            self.countChanged.emit(self.length)

        self.driver.quit()


class Ui_MainWindow(object):
    def __init__(self):
        with open('songs.json') as infile:
            self.songs = json.load(infile)
        self.index = int(len(self.songs) / 2)

    def onButtonClick(self):
        self.calc1 = ReMuse(self.songs[:self.index])
        self.calc2 = ReMuse(self.songs[self.index:])
        self.calc1.countChanged.connect(self.onCountChanged)
        self.calc2.countChanged.connect(self.onCountChanged)
        self.calc1.start()
        self.calc2.start()

    def onCountChanged(self, lenlist):
        self.pbar.setValue(self.pbar.value() + 100/2/lenlist) # 100 / num(threads) / len(list)
        print(f"Added %: {100/2/lenlist}\n"
              f"Current: {self.pbar.value()}")
        if self.pbar.value() == 100:
            self.label_6.setText("Completed")






    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        ###### Welcome Page (Frame 1)
        self.welcome = QtWidgets.QFrame(self.centralwidget)
        self.welcome.setEnabled(True)
        self.welcome.setGeometry(QtCore.QRect(10, 10, 931, 521))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(30)
        self.welcome.setFont(font)
        self.welcome.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.welcome.setFrameShadow(QtWidgets.QFrame.Raised)
        self.welcome.setObjectName("welcome")
        
        self.label = QtWidgets.QLabel(self.welcome)
        self.label.setEnabled(False)
        self.label.setGeometry(QtCore.QRect(160, 210, 621, 111))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        ###### Browsing Page (Frame 2)
        self.browse = QtWidgets.QFrame(self.centralwidget)
        self.browse.setGeometry(QtCore.QRect(10, 10, 931, 521))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.browse.setFont(font)
        self.browse.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.browse.setFrameShadow(QtWidgets.QFrame.Raised)
        self.browse.setObjectName("browse")
        self.label_3 = QtWidgets.QLabel(self.browse)
        self.label_3.setEnabled(False)
        self.label_3.setGeometry(QtCore.QRect(160, 20, 621, 111))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.browse)
        self.label_4.setGeometry(QtCore.QRect(270, 120, 391, 71))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(12)
        font.setItalic(True)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")

        self.textbox = QLineEdit(self.browse)
        self.textbox.move(280, 280)
        self.textbox.resize(280,40)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setItalic(True)
        self.textbox.setFont(font)
        self.textbox.setObjectName("textbox")

        self.pushButton = QtWidgets.QPushButton(self.browse)
        self.pushButton.setGeometry(QtCore.QRect(640, 280, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")



        self.yesButton = QtWidgets.QPushButton(self.browse)
        self.yesButton.setGeometry(QtCore.QRect(640, 380, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.yesButton.setFont(font)
        self.yesButton.setObjectName("yesButton")

        self.noButton = QtWidgets.QPushButton(self.browse)
        self.noButton.setGeometry(QtCore.QRect(640, 480, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.noButton.setFont(font)
        self.noButton.setObjectName("noButton")




        ###### Progress Page (Frame 3)
        self.progress = QtWidgets.QFrame(self.centralwidget)
        self.progress.setGeometry(QtCore.QRect(20, 20, 931, 521))
        self.progress.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.progress.setFrameShadow(QtWidgets.QFrame.Raised)
        self.progress.setObjectName("progress")
        self.label_6 = QtWidgets.QLabel(self.progress)
        self.label_6.setGeometry(QtCore.QRect(110, 190, 731, 121))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(22)
        font.setItalic(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)




        self.createGridLayout()
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.progress.setLayout(windowLayout)





        self.show_frame(3)
        self.yesButton.hide()
        self.noButton.hide()

        

        ## Progress bar
        self.pbar = QProgressBar(self.progress)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.pbar.setValue(0)

        self.btn = QPushButton('Begin Search', self.progress)
        self.btn.move(40, 80)
        self.btn.clicked.connect(lambda: self.onButtonClick())


        
        # self.timer = QTimer()
        # self.timer.setSingleShot(True)
        # self.timer.singleShot(2000, lambda: self.browse_page()) # single timer
        # self.timer.timeout.connect(lambda: self.browse_page()) # repeating timer
        # self.timer.start(3000)



        # Buttons to run
        self.pushButton.clicked.connect(self.browse_folder)
        self.yesButton.clicked.connect(self.proceed)
        self.noButton.clicked.connect(self.denied)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        
        layout.addWidget(QPushButton('1'),0,0)
        layout.addWidget(QPushButton('2'),0,1)
        layout.addWidget(QPushButton('3'),0,2)
        layout.addWidget(QPushButton('4'),1,0)
        layout.addWidget(QPushButton('5'),1,1)
        layout.addWidget(QPushButton('6'),1,2)
        layout.addWidget(QPushButton('7'),2,0)
        layout.addWidget(QPushButton('8'),2,1)
        layout.addWidget(QPushButton('9'),2,2)
        
        self.horizontalGroupBox.setLayout(layout)


















    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Welcome to ReMuse, Tylee"))
        self.label.adjustSize()
        self.label_3.setText(_translate("MainWindow", "Welcome to ReMuse"))
        self.label_4.setText(_translate("MainWindow", "Browse folder or enter path to begin"))
        self.textbox.setText(_translate("MainWindow", "Enter path here..."))
        self.pushButton.setText(_translate("MainWindow", "Browse"))       
        self.label_6.setText(_translate("MainWindow", "Progress..."))

        self.yesButton.setText(_translate("MainWindow", "Yes"))
        self.noButton.setText(_translate("MainWindow", "No"))

    def browse_folder(self):
        self.folder = QFileDialog.getExistingDirectory() + "/"
        self.fileCount = len([fname for fname in os.listdir(self.folder) if ".mp3" in fname])

        if self.fileCount == 0:
            self.label_4.setText(f"Current folder: {self.folder}\n"
                                f"There are no music files in the current directory. Please re-select..")
            self.label_4.adjustSize()
        else:
            self.label_4.setText(f"Current folder: {self.folder}\n"
                                f"There are {self.fileCount} music files in the current directory. Proceed?")
            self.label_4.adjustSize()
            
            self.yesButton.show()
            self.noButton.show()
        # print(f"There are {count} music files in the current directory. Proceed?")
        # if yes, proceed to frame 3, get Json, run ReMuse
        # else no, remain @ frame 2 and hide buttons

    def proceed(self):
        print("Getting Json...")
        GetJson(self.folder)
        self.show_frame(3)

    def denied(self):
        self.label_4.setText(f"Please select a folder")        
        self.yesButton.hide()
        self.noButton.hide()


    def show_widget(self, widget, on):
        effect = QGraphicsOpacityEffect()
        effect.setOpacity(on)
        widget.setGraphicsEffect(effect)
        widget.show() if on else widget.hide()





    def show_frame(self, fnum):
        def frames(frame):
            a, b, c = frame
            switch(self.welcome, a)
            switch(self.browse, b)
            switch(self.progress, c)

        def switch(widget, on): # Turn on/off opacity, then show/hide
            effect = QGraphicsOpacityEffect()
            effect.setOpacity(on)
            widget.setGraphicsEffect(effect)
            widget.show() if on else widget.hide()

        # 1: Welcome page
        # 2: Browse page
        # 3: Progress page
        if fnum == 1:
            frames([1,0,0])
        elif fnum == 2:
            frames([0,1,0])
        elif fnum == 3:
            frames([0,0,1])

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    






















'''
    def init(self):
        a, b, c = [1,1,1]
        # Set all frame opacity to 0
        self.switch(self.welcome, 0)
        self.switch(self.browse, 0)
        self.switch(self.progress, 0)
        print("All pages has been turned off.")

        # (Welcome) Fade in + 2-3s hold + fade out
        # print(int(not 1))

        # (Welcome) Hide; (Browse) Show
        
        curr = time.time()
        self.timer = QTimer()
        # self.timer.start(3000)
        self.timer.setInterval(3000)
        self.timer.setSingleShot(True)
        self.timer.start()
        self.timer.timeout.connect(lambda: self.switch(self.welcome, 0))
        self.timer.timeout.connect(lambda: print(f"{time.time() - curr} after alleged 3s"))

        QtWidgets.qApp.processEvents()
        self.timer.setInterval(3000)
        self.timer.setSingleShot(True)
        self.timer.start()
        self.timer.timeout.connect(lambda: self.switch(self.browse, 1))
        self.timer.timeout.connect(lambda: print(f"{time.time() - curr} after alleged 6s"))
        # print("hell yea")
        # self.timer.stop()

        # self.timer.start(5000)
        def count():
            print("Ready to browse folder...")
            print(f"{time.time() - curr} after alleged 5s")
        # self.timer.timeout.connect(lambda: count())

        # self.timer.singleShot(2000, lambda: self.turn_on(self.browse))
        # self.timer.singleShot(2000, lambda: count())
        # self.timer.stop()

        
        # self.a = QTimer()
        # self.a.singleShot(2000, lambda: self.switch(self.browse, 0))
        # # time.sleep(2)
        # # self.a = QTimer()
        # self.a.singleShot(4000, lambda: self.switch(self.browse, 1))

        # self.delay(self.switch(self.browse, 0), 0)
        # self.delay(self.switch(self.browse, 1), 3)
        # self.turn_on(self.browse)
    def delay(self, fxn, n):
        # time.sleep(2)
        timer = QTimer()
        timer.singleShot(2000*n, lambda: fxn)
        # timer.singleShot(2000, lambda: self.switch(self.browse, 0))
        # timer.singleShot(4000, lambda: self.switch(self.browse, 1))
        # print(f"{time.time() - self.curr} seconds have passed.")
    def browse_page(self):
        self.fade(self.welcome, 1000)
        self.timer.singleShot(1000, lambda: self.welcome.hide()) # single timer

        self.progress.hide()

        self.timer = QTimer()
        self.timer.singleShot(1000, lambda: self.unfade(self.browse, 1000)) # single timer
        
        # self.browse.hide()
        # self.progress.show()
        # self.hide_pls(self.progress)


        # self.unhide_pls(self.progress)
        # self.timer = QTimer()
        # self.timer.singleShot(1000, lambda: self.view_page()) # single timer
    def browse_button(self):
        # filename = QFileDialog.getOpenFileName()
        folder = QFileDialog.getExistingDirectory()
        print(f"My current folder: {folder}")
        for fname in os.listdir(folder + "/"):
            if ".mp3" in fname:
                # clean.Clean(fname).export_json()
                print(unidecode.unidecode(fname))
    def fade(self, widget, duration):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(duration)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()
    def unfade(self, widget, duration):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(duration)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        
        self.animation = QtCore.QPropertyAnimation(widget, b"geometry")
        self.animation.setDuration(duration+1000)
        self.animation.setStartValue(QRect(0, 0, 100, 100))
        self.animation.setEndValue(QRect(0, 0, 931, 521))



        self.animation.start()

'''