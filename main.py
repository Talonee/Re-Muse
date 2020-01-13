# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.welcome = QtWidgets.QFrame(self.centralwidget)
        self.welcome.setEnabled(True)
        self.welcome.setGeometry(QtCore.QRect(10, 10, 931, 521))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(36)
        self.welcome.setFont(font)
        self.welcome.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.welcome.setFrameShadow(QtWidgets.QFrame.Raised)
        self.welcome.setObjectName("welcome")
        self.label = QtWidgets.QLabel(self.welcome)
        self.label.setEnabled(False)
        self.label.setGeometry(QtCore.QRect(160, 210, 621, 111))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
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
        self.label_5 = QtWidgets.QLabel(self.browse)
        self.label_5.setGeometry(QtCore.QRect(200, 280, 441, 41))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setItalic(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
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



        # self.fade(self.label_3, 0)
        # self.fade(self.label_4, 0)
        # self.fade(self.label_5, 0)
        # self.fade(self.label_6, 0)
        # self.fade(self.pushButton, 0)

        # self.fade(self.browse, 0)
        self.hide_pls(self.browse)
        self.hide_pls(self.progress)
        
        self.timer = QTimer()
        self.timer.singleShot(2000, lambda: self.browse_page()) # single timer
        # self.browse_page()

        # self.timer.timeout.connect(lambda: self.browse_page()) # repeating timer
        # self.timer.start(3000)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def browse_page(self):
        self.fade(self.welcome, 1000)
        self.welcome.hide()

        self.progress.hide()

        self.timer = QTimer()
        self.timer.singleShot(1000, lambda: self.unfade(self.browse, 1000)) # single timer
        
        # self.unhide_pls(self.progress)
        # self.timer = QTimer()
        # self.timer.singleShot(1000, lambda: self.view_page()) # single timer
        
    def unhide_pls(self, widget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
        self.effect.setOpacity(1)

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
        self.animation.start()

    def hide_pls(self, widget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
        self.effect.setOpacity(0)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Welcome to ReMuse, whore.."))
        self.label.adjustSize()
        self.label_3.setText(_translate("MainWindow", "Welcome to ReMuse"))
        self.label_4.setText(_translate("MainWindow", "Browse folder or enter path to begin"))
        self.label_5.setText(_translate("MainWindow", "Enter path here..."))
        self.pushButton.setText(_translate("MainWindow", "Browse"))
        self.label_6.setText(_translate("MainWindow", "DaBop"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
