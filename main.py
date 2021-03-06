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
# from selenium.webdriver.support.ui  import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options


from mutagen.id3 import ID3, ID3NoHeaderError

import os, shutil, unidecode, time, json, urllib.request, sys, numpy

class ReMuse(QThread):
    countChanged = pyqtSignal(int) # must remain outside of init
    textChanged = pyqtSignal(str) # must remain outside of init
    finished = pyqtSignal() # must remain outside of init

    def __init__(self, songs, fin, fout):
        QThread.__init__(self)
        self.songs = songs
        self.length = len(self.songs)
        self.fin = fin
        self.fout = fout
             
    def run(self):
        # binary = r'C:\Users\Talon.Pollard\AppData\Local\Mozilla Firefox\firefox.exe' # Work dir
        binary = r'C:\Program Files\Mozilla Firefox\firefox.exe' # Home dir
        options = Options()
        options.set_headless(headless=True)
        options.binary = binary

        profile = webdriver.FirefoxProfile()
        profile.set_preference("media.volume_scale", "0.0")

        cap = DesiredCapabilities().FIREFOX
        cap["marionette"] = True #optional

        self.driver = webdriver.Firefox(firefox_profile=profile, options=options, capabilities=cap, executable_path="drivers/geckodriver.exe")
        self.driver.get("https://music.youtube.com/")
        self.driver.execute_script("window.open('http://www.google.com/');")        
        time.sleep(10)

        for song in self.songs:
            fname = unidecode.unidecode(song["File"])
            self.textChanged.emit(fname)
            Search(self.driver, song, self.fin, self.fout).find()
            self.countChanged.emit(self.length)

        self.driver.quit()
        self.finished.emit()


class Ui_MainWindow(object):
    MAX_THREAD = 2
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    FRAME_DIM = [0, 0, WINDOW_WIDTH, WINDOW_HEIGHT]

    def __init__(self):
        self.errorMsg = set()
        self.fin = ""
        self.fout = ""
        self.iter = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

    ###### Welcome Page (Frame 1)
        self.welcome = QtWidgets.QFrame(self.centralwidget)
        self.welcome.setGeometry(QtCore.QRect(*self.FRAME_DIM))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(40)
        self.welcome.setFont(font)
        self.welcome.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.welcome.setFrameShadow(QtWidgets.QFrame.Raised)
        self.welcome.setObjectName("welcome")
        self.label = QtWidgets.QLabel(self.welcome)
        self.label.setText("Welcome to ReMuse")
        self.label.adjustSize()
        posX = self.welcome.rect().width() / 2 - self.label.rect().width() / 2
        posY = self.welcome.rect().height() / 2 - self.label.rect().height() / 2
        self.label.move(posX, posY)
        self.label.setObjectName("label")

    ###### Browsing Page (Frame 2)
        self.browse = QtWidgets.QFrame(self.centralwidget)
        self.browse.setGeometry(QtCore.QRect(*self.FRAME_DIM))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.browse.setFont(font)
        self.browse.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.browse.setFrameShadow(QtWidgets.QFrame.Raised)
        self.browse.setObjectName("browse")

        self.label_3 = QtWidgets.QLabel(self.browse)
        font.setPointSize(35)
        self.label_3.setFont(font)
        self.label_3.setText("ReMuse")
        self.label_3.adjustSize()
        posX = self.browse.rect().width() / 2 - self.label_3.rect().width() / 2
        posY = self.browse.rect().height() * 0.15
        self.label_3.move(posX, posY)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.browse)
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setText("Browse folder or enter a path to begin")
        self.label_4.adjustSize()
        posX = self.browse.rect().width() / 2 - self.label_4.rect().width() / 2
        posY = self.browse.rect().height() * 0.35
        self.label_4.move(posX, posY)
        self.label_4.setObjectName("label_4")

        self.inputText = QLineEdit(self.browse)
        font.setPointSize(10)
        self.inputText.setFont(font)
        self.inputText.setPlaceholderText("Input folder")
        self.inputText.setObjectName("inputText")

        self.outputText = QLineEdit(self.browse)
        font.setPointSize(10)
        self.outputText.setFont(font)
        self.outputText.setPlaceholderText("Output folder")
        self.outputText.setObjectName("outputText")

        self.browseInput = QtWidgets.QPushButton(self.browse)
        font.setPointSize(10)
        self.browseInput.setFont(font)
        self.browseInput.setText("Browse")
        self.browseInput.setObjectName("browseInput")

        self.browseOutput = QtWidgets.QPushButton(self.browse)
        font.setPointSize(10)
        self.browseOutput.setFont(font)
        self.browseOutput.setText("Browse")
        self.browseOutput.setObjectName("browseOutput")

        self.total = QGroupBox(self.browse)
        vbox = QVBoxLayout()     
        inp = QHBoxLayout()
        inp.addWidget(self.inputText)
        inp.addWidget(self.browseInput)    
        out = QHBoxLayout()
        out.addWidget(self.outputText)
        out.addWidget(self.browseOutput)
        vbox.addLayout(inp)
        vbox.addLayout(out)
        vbox.setSpacing(20)
        self.total.setLayout(vbox)

        self.total.resize(self.WINDOW_WIDTH * 0.5, self.inputText.rect().height() * 2 + 50 + vbox.spacing())
        posX = self.browse.rect().width() / 2 - self.total.rect().width() / 2
        posY = self.browse.rect().height() * 0.45
        self.total.move(posX, posY)
        self.total.setObjectName("total")
        
        self.yesButton = QtWidgets.QPushButton(self.browse)
        font.setPointSize(10)
        posX = self.browse.rect().width() / 2  - self.yesButton.rect().width() / 2 - 75
        posY = self.browse.rect().height() * 0.67
        self.yesButton.move(posX, posY)
        self.yesButton.setFont(font)
        self.yesButton.setText("Proceed")
        self.yesButton.setObjectName("yesButton")
        self.yesButton.setDisabled(True)

        self.noButton = QtWidgets.QPushButton(self.browse)
        font.setPointSize(10)
        posX = self.browse.rect().width() / 2  - self.noButton.rect().width() / 2 + 75
        posY = self.browse.rect().height() * 0.67
        self.noButton.move(posX, posY)
        self.noButton.setFont(font)        
        self.noButton.setText("Cancel")
        self.noButton.setObjectName("noButton")
        self.noButton.setDisabled(True)

        # Browse Frame::Buttons
        self.inputText.textChanged.connect(self.dirValidity)
        self.outputText.textChanged.connect(self.dirValidity)
        self.browseInput.clicked.connect(self.browse_folder)
        self.browseOutput.clicked.connect(self.browse_folder)
        self.yesButton.clicked.connect(self.proceed)
        self.noButton.clicked.connect(self.cancel)
        
    ###### Progress Page (Frame 3)
        self.progress = QtWidgets.QFrame(self.centralwidget)
        self.progress.setGeometry(QtCore.QRect(*self.FRAME_DIM))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(11)
        self.progress.setFont(font)
        self.progress.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.progress.setFrameShadow(QtWidgets.QFrame.Raised)
        self.progress.setObjectName("progress")

        ## Progress bar
        self.pbar = QProgressBar(self.progress)
        self.pbar.setGeometry(0, 0, self.WINDOW_WIDTH * 0.6, 25)
        self.pbar.setValue(0)
        posX = self.progress.rect().width() / 2 - self.pbar.rect().width() / 2
        posY = self.progress.rect().height() * 0.45
        self.pbar.move(posX, posY)

        self.btn = QPushButton('Begin Search', self.progress)
        self.btn.setGeometry(0, 0, 150, 38)
        posX = self.progress.rect().width() / 2 - self.btn.rect().width() / 2
        posY = self.progress.rect().height() * 0.52
        self.btn.move(posX, posY)
        self.btn.clicked.connect(self.onButtonClick)

        self.label_6 = QtWidgets.QLabel(self.progress)
        self.label_6.setText("In progress...")
        posX = self.progress.rect().width() / 2 - self.label_6.rect().width() / 2
        posY = self.progress.rect().height() * 0.39
        self.label_6.move(posX, posY)
        self.label_6.setObjectName("label_6")
        self.label_6.hide()

    ###### Review Page (Frame 4)
        self.review = QtWidgets.QFrame(self.centralwidget)
        self.review.setGeometry(QtCore.QRect(*self.FRAME_DIM))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.review.setFont(font)
        self.review.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.review.setFrameShadow(QtWidgets.QFrame.Raised)
        self.review.setObjectName("review")

        # Welcome and transition to browsing page
        self.landing()

        # self.show_frame(4)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

######### FRAME 1 ############
    def landing(self):
        self.show_frame(1)
        timer = QTimer()
        timer.singleShot(1500, lambda: self.show_frame(2))

######### FRAME 2 ############
    def browse_folder(self):
        self.folder = QFileDialog.getExistingDirectory() + "/"
        obj = self.browse.sender().objectName()

        if not (self.folder == "/"):
            if obj == "browseInput":
                    self.inputText.setText(self.folder)  
            elif obj == "browseOutput":
                self.outputText.setText(self.folder)
    
    def dirValidity(self):
        # Check and enter info into error msg first
        self.errorMsg.clear()
        if self.inputText.text() and self.outputText.text():
            self.yesButton.setEnabled(True)
            self.noButton.setEnabled(True)
            self.fin = self.inputText.text()
            self.fout = self.outputText.text()

            # Input test cases
            if not os.path.isdir(self.fin):
                self.errorMsg.add("- Invalid input path.\n")
            else:
                self.fCount = len([fname for fname in os.listdir(self.fin) if ".mp3" in fname])
                if self.fCount == 0:
                    self.errorMsg.add("- No music files found. Re-select input folder..\n")

            # Output test cases
            if not os.path.isdir(self.fout):
                self.errorMsg.add("- Invalid output path.\n")
        else:
            self.yesButton.setDisabled(True)

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("An error(s) has occurred:")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setInformativeText("".join(self.errorMsg))
        msg.exec_()

    def proceed(self):
        if self.errorMsg:
            self.show_popup()
            self.yesButton.setDisabled(True)
            self.noButton.setDisabled(True)
        else:
            self.show_frame(3)
            self.songs = GetJson(self.fin).songs
            self.index = int(len(self.songs) / 2)

    def cancel(self):
        self.inputText.clear()
        self.outputText.clear()
        self.yesButton.setDisabled(True)
        self.noButton.setDisabled(True)

######### FRAME 3 ############
    def onButtonClick(self):
        self.completedThread = 0
        self.label_6.show()

        self.calc1 = ReMuse(self.songs[:self.index], self.fin, self.fout)
        self.calc2 = ReMuse(self.songs[self.index:], self.fin, self.fout)
        
        self.calc1.textChanged.connect(self.onTextChanged)
        self.calc1.countChanged.connect(self.onCountChanged)
        self.calc1.finished.connect(self.finishedThread)

        self.calc2.textChanged.connect(self.onTextChanged)
        self.calc2.countChanged.connect(self.onCountChanged)
        self.calc2.finished.connect(self.finishedThread)

        self.calc1.start()
        self.calc2.start()
        
    def onTextChanged(self, fname):
        self.iter += 1
        updateText = f"Searching data for \"{fname[:-4]}...\" ({self.iter}/{len(self.songs)})"
        self.label_6.setText(updateText)
        self.label_6.adjustSize()
        posX = self.progress.rect().width() / 2 - self.label_6.rect().width() / 2
        posY = self.progress.rect().height() * 0.39
        self.label_6.move(posX, posY)

    def onCountChanged(self, lenlist):
        self.pbar.setValue(self.pbar.value() + 100/2/lenlist) # 100 / num(threads) / len(list)
        
        # print(f"Added %: {100/2/lenlist}\n"
        #       f"Current: {self.pbar.value()}")

    def finishedThread(self):
        self.completedThread += 1 
        if self.completedThread == self.MAX_THREAD:
            self.pbar.setValue(100)
            self.label_6.setText("Completed")
            self.getImages()
            self.griddy()
            self.scrolly()
            self.show_frame(4)

######### FRAME 4 ############
    def scrolly(self):
        self.scroll = QScrollArea(self.review)           
        self.widget = QWidget()
        self.widget.setLayout(self.mama_grid)

        self.scroll.setGeometry(*self.FRAME_DIM)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        if self.reviewRow <= 2:
            self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

    def griddy(self):
        self.mama_grid = QtWidgets.QGridLayout()

        position = []
        for row in range(self.reviewRow): # change range to adapt
            for col in range(self.reviewCol):
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
        
        covSrc = self.fout + "covers/"
        self.numItems = len(os.listdir(covSrc))

        size = 300 if self.numItems <= 3 else 225
        self.reviewRow = int(self.numItems / 3) if (self.numItems % 3 == 0) else int(self.numItems / 3 + 1) 
        self.reviewCol = int(3) if (self.numItems <= 7) else int(4)

        for fname in os.listdir(self.fout):
            if ".mp3" in fname:
                id3 = ID3(f"{self.fout}{fname}")
                img = QtWidgets.QLabel()
                cov = id3["TALB"][0][:15] + ".jpg"
                pixmap = QtGui.QPixmap(f"{covSrc}{cov}").scaledToWidth(size)
                img.setPixmap(pixmap)
                txt = QtWidgets.QLabel()
                txt.setText(id3['TIT2'][0])
                txt.setAlignment(Qt.AlignCenter)
                self.container.append((img, txt))

######### MISCELLANEOUS ############
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
            widget.setEnabled(on)
        
        matrix = numpy.identity(4, int)
        frames(matrix[fnum - 1])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    



'''
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

'''
    # def __init__(self):
        # with open('songs.json') as infile:
        #     self.songs = json.load(infile)
        # self.songs = []

       
        # self.timer = QTimer()
        # self.timer.setSingleShot(True)
        # self.timer.singleShot(2000, lambda: self.browse_page()) # single timer
        # self.timer.timeout.connect(lambda: self.browse_page()) # repeating timer
        # self.timer.start(3000)
'''