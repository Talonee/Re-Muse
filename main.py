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

from mutagen.id3 import ID3, ID3NoHeaderError

import os, shutil, unidecode, time, json, urllib.request, sys, numpy

class ReMuse(QThread):
    countChanged = pyqtSignal(int) # must remain outside of init
    finished = pyqtSignal() # must remain outside of init

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
            print(f"Finished {mehoy}")
            self.countChanged.emit(self.length)

        self.driver.quit()
        self.finished.emit()


class Ui_MainWindow(object):
    MAX_THREAD = 2

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1280, 720)
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

        self.yesButton.hide()
        self.noButton.hide()

        # Buttons to run
        self.pushButton.clicked.connect(self.browse_folder)
        self.yesButton.clicked.connect(self.proceed)
        self.noButton.clicked.connect(self.denied)



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

        ## Progress bar
        self.pbar = QProgressBar(self.progress)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.pbar.setValue(0)

        self.btn = QPushButton('Begin Search', self.progress)
        self.btn.move(40, 80)
        self.btn.clicked.connect(lambda: self.onButtonClick())



        ###### Review Page (Frame 4)
        self.review = QtWidgets.QFrame(self.centralwidget)
        self.review.setGeometry(QtCore.QRect(20, 20, 931, 521))
        self.review.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.review.setFrameShadow(QtWidgets.QFrame.Raised)
        self.review.setObjectName("review")



        # Welcome and transition to browsing page
        self.landing()



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

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


    ######### FRAME 1 ############
    def landing(self):
        self.show_frame(1)
        timer = QTimer()
        timer.singleShot(3000, lambda: self.show_frame(2))

    ######### FRAME 2 ############
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

    def proceed(self):
        self.show_frame(3)
        # print("Getting lists...") # update label 4
        self.songs = GetJson(self.folder).songs
        self.index = int(len(self.songs) / 2)

    def denied(self):
        self.label_4.setText(f"Please select a folder")        
        self.yesButton.hide()
        self.noButton.hide()

    ######### FRAME 3 ############
    def onButtonClick(self):
        self.completedThread = 0

        self.calc1 = ReMuse(self.songs[:self.index])
        self.calc2 = ReMuse(self.songs[self.index:])
        
        self.calc1.countChanged.connect(self.onCountChanged)
        self.calc1.finished.connect(self.finishedThread)

        self.calc2.countChanged.connect(self.onCountChanged)
        self.calc2.finished.connect(self.finishedThread)

        self.calc1.start()
        self.calc2.start()
        
    def onCountChanged(self, lenlist):
        self.pbar.setValue(self.pbar.value() + 100/2/lenlist) # 100 / num(threads) / len(list)
        # print(f"Added %: {100/2/lenlist}\n"
        #       f"Current: {self.pbar.value()}")

    def finishedThread(self):
        self.completedThread += 1 
        if self.completedThread == self.MAX_THREAD:
            self.pbar.setValue(100)
            self.label_6.setText("Retrieving progress...")
            self.getImages()
            self.griddy()
            self.scrolly()
            self.show_frame(4)

    ######### FRAME 4 ############
    def scrolly(self):
        self.scroll = QScrollArea(self.review)           
        self.widget = QWidget()
        self.widget.setLayout(self.mama_grid)

        self.scroll.setGeometry(50, 20, 800, 500)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

    def griddy(self):
        self.mama_grid = QtWidgets.QGridLayout()

        position = []
        for row in range(7): # change range to adapt
            for col in range(3):
                position.append((row, col))

        for item, pos in zip(self.container, position):
            groupBox = QGroupBox()
            vbox = QVBoxLayout()
            vbox.addWidget(item[0])
            vbox.addWidget(item[1])
            groupBox.setLayout(vbox)
            self.mama_grid.addWidget(groupBox, *pos)
                
        self.mama_grid.setAlignment(Qt.AlignCenter)

    def getImages(self):
        self.container = []
        self.length = len(os.listdir("covers/")) # dir is your directory path
       
        for fname in os.listdir("final/"):
            if ".mp3" in fname:
                id3 = ID3(f"final/{fname}")
                img = QtWidgets.QLabel()
                cov = id3["TALB"][0][:15] + ".jpg"
                pixmap = QtGui.QPixmap(f"covers/{cov}").scaledToWidth(200)
                img.setPixmap(pixmap)
                txt = QtWidgets.QLabel()
                txt.setText(id3['TIT2'][0])
                txt.setAlignment(Qt.AlignCenter)
                self.container.append((img, txt))

        # for fname in os.listdir("covers/"):
        #     if ".jpg" in fname:
        #         img = QtWidgets.QLabel()
        #         pixmap = QtGui.QPixmap(f"covers/{fname}").scaledToWidth(200)
        #         img.setPixmap(pixmap)
        #         txt = QtWidgets.QLabel()
        #         txt.setText(fname[:-4])
        #         txt.setAlignment(Qt.AlignCenter)
        #         self.container.append((img, txt))







    def show_widget(self, widget, on):
        effect = QGraphicsOpacityEffect()
        effect.setOpacity(on)
        widget.setGraphicsEffect(effect)
        widget.show() if on else widget.hide()


    def show_frame(self, fnum):
        def frames(frame):
            a, b, c, d = frame
            switch(self.welcome, a)
            switch(self.browse, b)
            switch(self.progress, c)
            switch(self.review, d)

        def switch(widget, on): # Turn on/off opacity, then show/hide
            effect = QGraphicsOpacityEffect()
            effect.setOpacity(on)
            widget.setGraphicsEffect(effect)
            widget.show() if on else widget.hide()
        
        # 1: Welcome page
        # 2: Browse page
        # 3: Progress page
        matrix = numpy.identity(4, int)
        frames(matrix[fnum - 1])




    # def __init__(self):
        # with open('songs.json') as infile:
        #     self.songs = json.load(infile)
        # self.songs = []

    
        
        # self.timer = QTimer()
        # self.timer.setSingleShot(True)
        # self.timer.singleShot(2000, lambda: self.browse_page()) # single timer
        # self.timer.timeout.connect(lambda: self.browse_page()) # repeating timer
        # self.timer.start(3000)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    









        # items = [(1,2), (4,1), (9,7), (0,4), (6,4), (4,3)]
        # position = []
        # for row in range(2):
        #     for col in range(3):
        #         position.append((row, col))

        # for item, pos in zip(items, position):
        #     print(*pos)














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
'''
#################################################
    def createGridLayout(self):
        self.image = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("covers/Clueless.jpg")
        # pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        pixmap = pixmap.scaledToHeight(200)
        self.image.setPixmap(pixmap)
        # self.image.setScaledContents(True)
        self.text = QtWidgets.QLabel()
        # self.text.setText("ORA ORA ORA ORA ORA ORA ORA ORA ORA ORA ORA ORA")
        self.text.setText("Clueless")
        self.text.setAlignment(Qt.AlignCenter)

        self.image1 = QtWidgets.QLabel(self.centralwidget)
        pixmap = QtGui.QPixmap("covers/Badunkadunk.jpg")
        # pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
        pixmap = pixmap.scaledToHeight(200)
        self.image1.setPixmap(pixmap)
        self.image1.setScaledContents(True)
        self.text1 = QtWidgets.QLabel(self.centralwidget)
        self.text1.setText("Badunkadunk")
        self.text1.setAlignment(Qt.AlignCenter)

        self.image2 = QtWidgets.QLabel(self.centralwidget)
        pixmap = QtGui.QPixmap("covers/GOKU.jpg")
        pixmap = pixmap.scaledToHeight(200)
        self.image2.setPixmap(pixmap)
        self.image2.setScaledContents(True)
        self.text2 = QtWidgets.QLabel(self.centralwidget)
        self.text2.setText("GOKU")
        self.text2.setAlignment(Qt.AlignCenter)

        self.image3 = QtWidgets.QLabel(self.centralwidget)
        pixmap = QtGui.QPixmap("covers/Wafia.jpg")
        pixmap = pixmap.scaledToHeight(200)
        self.image3.setPixmap(pixmap)
        self.image3.setScaledContents(True)
        self.text3 = QtWidgets.QLabel(self.centralwidget)
        self.text3.setText("Wafia")
        self.text3.setAlignment(Qt.AlignCenter)




        # self.text2.setText("WRRRRRRRRRRRRRRYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")




        grid_layout = QtWidgets.QGridLayout(self.centralwidget)
        # self.centralwidget.setLayout(grid_layout)
        # grid_layout.setColumnStretch(1, 1)
        # grid_layout.setRowStretch(1, 1)
        # grid_layout.setGeometry(QtCore.QRect(100, 100, 100, 100))
        # grid_layout.addWidget(self.image, 0, 0)
        # grid_layout.addWidget(self.text, 1, 0)
        # grid_layout.addWidget(self.image1, 0, 1)
        # grid_layout.addWidget(self.text1, 2, 1)
        # for row in range(3):
        #     for col in range(3):
        #         grid_layout.addWidget(QPushButton(str(row + col)), row, col)

        groupBox = QGroupBox()
        vbox = QVBoxLayout()
        vbox.addWidget(self.image)
        vbox.addWidget(self.text)
        # vbox.addStretch(1)
        groupBox.setLayout(vbox)

        groupBox1 = QGroupBox()
        vbox = QVBoxLayout()
        vbox.addWidget(self.image1)
        vbox.addWidget(self.text1)
        # vbox.addStretch(1)
        groupBox1.setLayout(vbox)

        groupBox2 = QGroupBox()
        vbox = QVBoxLayout()
        vbox.addWidget(self.image2)
        vbox.addWidget(self.text2)
        # vbox.addStretch(1)
        groupBox2.setLayout(vbox)

        groupBox3 = QGroupBox()
        vbox = QVBoxLayout()
        vbox.addWidget(self.image3)
        vbox.addWidget(self.text3)
        # vbox.addStretch(1)
        groupBox3.setLayout(vbox)


        grid_layout.addWidget(groupBox, 0, 0)
        grid_layout.addWidget(groupBox1, 1, 0)
        grid_layout.addWidget(groupBox2, 2, 0)
        grid_layout.addWidget(groupBox3, 3, 0)
        
        grid_layout.setAlignment(Qt.AlignCenter)




        self.scroll = QScrollArea(self.centralwidget)             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.widget.setLayout(grid_layout)

        self.scroll.setGeometry(200, 100, 500, 500)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        # self.scroll.setWidget(grid_layout)
        # self.scroll.setAlignment(Qt.AlignCenter)







        # mama_grid = QtWidgets.QGridLayout()
        # mama_grid.setColumnStretch(3, 3)
        # mama_grid.setRowStretch(3, 3)
        # self.centralwidget.setLayout(mama_grid)
        # mama_grid.addWidget(grid_layout, 0, 0)
        # mama_grid.addLayout(grid_layout, 0, 0)
        # mama_grid.addItem(grid_layout, 0, 0)
        # mama_grid.addLayout(grid_layout, 0, 1)
        # mama_grid.addWidget(self.text, 1, 0)






        # title = QLabel('Title')
        # author = QLabel('Author')
        # review = QLabel('Review')
        # test = QLabel('Test')

        # titleEdit = QLineEdit()
        # authorEdit = QLineEdit()
        # reviewEdit = QTextEdit()

        # grid = QGridLayout()
        # grid.setSpacing(10)

        # # grid.addWidget(photo, 0, 0)

        # grid.addWidget(title, 1, 0)
        # grid.addWidget(titleEdit, 1, 1)

        # grid.addWidget(author, 2, 0)
        # grid.addWidget(authorEdit, 2, 1)

        # grid.addWidget(review, 3, 0)
        # grid.addWidget(reviewEdit, 3, 1, 5, 1)

        # grid.addWidget(test, 5, 0)
        
        # self.progress.setLayout(grid) 
##################################################
'''