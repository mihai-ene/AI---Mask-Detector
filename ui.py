from PyQt5 import QtCore, QtGui, QtWidgets
from  PyQt5.QtGui import QPixmap, QImage
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowFlag(Qt.FramelessWindowHint)
        MainWindow.setFixedSize(627, 559)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.cameraLabel = QtWidgets.QLabel(self.centralwidget)
        self.cameraLabel.setGeometry(QtCore.QRect(60, 150, 511, 301))
        self.cameraLabel.setStyleSheet("")
        self.cameraLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.cameraLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cameraLabel.setStyleSheet("border: 1px solid #77b6a8;")
        self.cameraLabel.setText("")
        self.cameraLabel.setObjectName("cameraLabel")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 10, 571, 331))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.backgroundimg = QtWidgets.QLabel(self.centralwidget)
        pixmap = QPixmap('img/UI.png')
        self.backgroundimg.setPixmap(pixmap)
        self.backgroundimg.resize(pixmap.width(), pixmap.height())
        self.startButton = QtWidgets.QLabel(self.centralwidget)
        pixmap = QPixmap('img/START.png')
        self.startButton.setGeometry(QtCore.QRect(245, 470, 131, 31))
        self.startButton.setPixmap(pixmap)
        self.startButton.resize(pixmap.width(), pixmap.height())
        self.closeButton = QtWidgets.QLabel(self.centralwidget)
        pixmap = QPixmap('img/Close.png')
        self.closeButton.setGeometry(QtCore.QRect(585, 10, 131, 31))
        self.closeButton.setPixmap(pixmap)
        self.closeButton.resize(pixmap.width(), pixmap.height())
        self.cameraLabel.raise_()
        self.label_2.raise_()
        self.startButton.raise_()
        self.closeButton.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 627, 25))
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




#import btn_rc
#import img_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet('QMainWindow{background-color: #0b6c59;border: 0px solid black;}')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

