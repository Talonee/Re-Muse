# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test2.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(587, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(10, 10, 431, 531))
        self.photo.setText("")
        self.photo.setPixmap(QtGui.QPixmap("../../../Pictures/Suzii/WhatsApp Image 2019-07-27 at 23.18.40.jpeg"))
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")

        self.suzii1 = QtWidgets.QPushButton(self.centralwidget)
        self.suzii1.setGeometry(QtCore.QRect(470, 90, 93, 28))
        self.suzii1.setObjectName("suzii1")

        self.suzii2 = QtWidgets.QPushButton(self.centralwidget)
        self.suzii2.setGeometry(QtCore.QRect(470, 280, 93, 28))
        self.suzii2.setObjectName("suzii2")

        self.button = QtWidgets.QPushButton(self.centralwidget)
        self.button.setGeometry(QtCore.QRect(470, 470, 93, 28))
        self.button.setObjectName("button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 587, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.suzii1.clicked.connect(lambda: self.show_s1())
        self.suzii2.clicked.connect(lambda: self.show_s2())

        self.button.clicked.connect(lambda: self.show_popup())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.suzii1.setText(_translate("MainWindow", "Suzii"))
        self.suzii2.setText(_translate("MainWindow", "Also Suzii"))
        self.button.setText(_translate("MainWindow", "Random Button"))

    def show_s1(self):
        self.photo.setPixmap(QtGui.QPixmap("../../../Pictures/Suzii/WhatsApp Image 2019-07-27 at 23.18.40.jpeg"))

    
    def show_s2(self):
        self.photo.setPixmap(QtGui.QPixmap("../../../Pictures/Suzii/WhatsApp Image 2019-07-27 at 23.20.30.jpeg"))

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Browse Folder")
        msg.setText("Yea aight")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Cancel|QMessageBox.Ignore|QMessageBox.Retry)
        msg.setDefaultButton(QMessageBox.Ignore)
        msg.setInformativeText("something something, informative!")
        
        msg.setDetailedText("details")

        msg.buttonClicked.connect(self.popup_button)

        x = msg.exec_()


    def popup_button(self, i):
        print(i.text())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
