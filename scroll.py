# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scroll.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.verticalScrollBar.setGeometry(QtCore.QRect(770, 10, 16, 521))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 741, 521))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 739, 519))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 701, 171))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 3, 1, 1)



        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        # self.imageLabel.setGeometry(QtCore.QRect(10, 10, 200, 200))
        self.imageLabel.setPixmap(QtGui.QPixmap("covers/Badunkadunk.jpg"))
        self.imageLabel.setScaledContents(True)
        self.gridLayout.addWidget(self.imageLabel, 0, 1, 1, 1)

        self.imageLabel1 = QtWidgets.QLabel(self.centralwidget)
        # self.imageLabel1.setGeometry(QtCore.QRect(10, 10, 200, 200))
        self.imageLabel1.setPixmap(QtGui.QPixmap("covers/Clueless.jpg"))
        self.imageLabel1.setScaledContents(True)
        self.gridLayout.addWidget(self.imageLabel1, 0, 2, 1, 1)

        self.imageLabel2 = QtWidgets.QLabel(self.centralwidget)
        # self.imageLabel2.setGeometry(QtCore.QRect(10, 10, 200, 200))
        self.imageLabel2.setPixmap(QtGui.QPixmap("covers/Skin.jpg"))
        self.imageLabel2.setScaledContents(True)
        self.gridLayout.addWidget(self.imageLabel2, 0, 3, 1, 1)

        self.imageLabel3 = QtWidgets.QLabel(self.centralwidget)
        # self.imageLabel3.setGeometry(QtCore.QRect(10, 10, 200, 200))
        self.imageLabel3.setPixmap(QtGui.QPixmap("covers/Skin.jpg"))
        self.imageLabel3.setScaledContents(True)
        self.gridLayout.addWidget(self.imageLabel3, 0, 4, 1, 1)

        # self.graphicsView_2 = QtWidgets.QGraphicsView(self.gridLayoutWidget)
        # self.graphicsView_2.setObjectName("graphicsView_2")
        # self.gridLayout.addWidget(self.graphicsView_2, 0, 1, 1, 1)

        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(self.gridLayoutWidget)
        self.graphicsView.setEnabled(True)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.graphicsView_3 = QtWidgets.QGraphicsView(self.gridLayoutWidget)
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.gridLayout.addWidget(self.graphicsView_3, 0, 2, 1, 1)
        self.graphicsView_4 = QtWidgets.QGraphicsView(self.gridLayoutWidget)
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.gridLayout.addWidget(self.graphicsView_4, 0, 4, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 4, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.scrollArea.raise_()
        self.verticalScrollBar.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "TextLabel"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
