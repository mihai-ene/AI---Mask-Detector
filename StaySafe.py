from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtGui import *
from PyQt5.QtCore import QSize
import cv2, imutils
import threading
import playsound
import time
import numpy as np
from tensorflow import keras
import pyshine as ps


faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(887, 729)
        MainWindow.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.backgroundimg = QtWidgets.QLabel(self.centralwidget)
        pixmap = QPixmap('img/UI.png')
        self.backgroundimg.setPixmap(pixmap)
        self.backgroundimg.resize(pixmap.width(), pixmap.height())


        self.cameraPlace = QtWidgets.QLabel(self.centralwidget)
        self.cameraPlace.setText("")
        self.cameraPlace.setPixmap(QtGui.QPixmap(""))
        self.cameraPlace.setFrameShape(QtWidgets.QFrame.Box)
        self.cameraPlace.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cameraPlace.setStyleSheet("border: 3px solid #77b6a8;")
        self.cameraPlace.setObjectName("cameraPlace")
        self.cameraPlace.setGeometry(QtCore.QRect(88, 130, 711, 501))

        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(375, 660, 132, 31))
        icon = QIcon('img/START.png')
        self.startButton.setIcon(icon)
        self.startButton.setIconSize(QSize(132, 31))
        self.startButton.setObjectName("startButton")
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setGeometry(QtCore.QRect(850, 10, 24, 24))
        icon = QIcon('img/Close.png')
        self.closeButton.setIcon(icon)
        self.closeButton.setIconSize(QSize(132, 31))
        self.closeButton.setObjectName("closeButton")
        self.soundButton = QtWidgets.QPushButton(self.centralwidget)
        self.soundButton.setGeometry(QtCore.QRect(15, 18, 28, 25))
        icon = QIcon('img/MutedSound.png')
        self.soundButton.setIcon(icon)
        self.soundButton.setIconSize(QSize(132, 31))
        self.soundButton.setObjectName("soundButton")
        self.gridButton = QtWidgets.QPushButton(self.centralwidget)
        self.gridButton.setGeometry(QtCore.QRect(65, 12, 39, 36))
        icon = QIcon('img/GridON.png')
        self.gridButton.setIcon(icon)
        self.gridButton.setIconSize(QSize(39, 36))
        self.gridButton.setObjectName("gridButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.startButton.clicked.connect(self.loadImage)
        self.closeButton.clicked.connect(self.closeWindow)
        self.soundButton.clicked.connect(self.sound)
        self.gridButton.clicked.connect(self.gridUpdate)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.tmp = None
        self.started = False
        self.soundOn = False
        self.prediction = "NOT SAFE"
        self.windowIsOpened = True
        self.lastplayed = 0
        self.lastpredicted = 0
        self.gridOn = True
        self.PhotoSet = False
        self.isThereAFace = True

        self.model = keras.models.load_model('IA - MaskDetector.h5')
    def gridUpdate(self):

        """
        This function will check if the gridButton is pressed or not,
        in order to know if the grid must be turned ON or OFF
        """

        if self.gridOn: # That means we want to disable the grid if the button is clicked
            self.gridOn = False
            icon = QIcon('img/GridOFF.png')
            self.gridButton.setIcon(icon)
            self.gridButton.setIconSize(QSize(39, 36))
        else:
            self.gridOn = True # That means we want to enable the grid if the button is clicked
            icon = QIcon('img/GridON.png')
            self.gridButton.setIcon(icon)
            self.gridButton.setIconSize(QSize(39, 36))

    def sound(self):

        """
        This function will check if the soundButton is pressed or not,
        in order to know if the sound must be turned ON or OFF
        """

        if self.soundOn: # That means we want to enable the sound if the button is clicked
            self.soundOn = False
            icon = QIcon('img/MutedSound.png')
            self.soundButton.setIcon(icon)
            self.soundButton.setIconSize(QSize(132, 31))
        else:
            self.soundOn = True # That means we want to disable the sound if the button is clicked
            icon = QIcon('img/UnmutedSound.png')
            self.soundButton.setIcon(icon)
            self.soundButton.setIconSize(QSize(132, 31))

    def play(self):
        playsound.playsound('Sound/wear.mp3')

    def predict(self,image):
        predictions = self.model.predict(image)
        if predictions > 0:
            self.prediction = "NOT SAFE"
        else:
            self.prediction = "SAFE"


    def loadImage(self):

        """
        This function will obtain the image from webcam
        and set it to label using the setPhoto function
        """

        if self.started: # That means the button "START" is pressed
            self.started = False
            icon = QIcon('img/START.png')
            self.startButton.setIcon(icon)
            self.startButton.setIconSize(QSize(132, 31))

        else: # That means the button "STOP" is pressed
            self.started = True
            self.PhotoSet = True
            icon = QIcon('img/STOP.png')
            self.startButton.setIcon(icon)
            self.startButton.setIconSize(QSize(132, 31))

        vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while True:
            img, self.image = vid.read()
            img = imutils.resize(self.image, height=480)

            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.1, 4)
            if len(faces) ==0:
                self.isThereAFace = False # That means there's nobody in front of WebCam
            else:
                self.isThereAFace = True # That means there's someone in front of WebCam
                for x, y, w, h in faces:
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_color = img[y:y + h, x:x + w]
                    if self.gridOn == True: # Drawing the rectangle around the face if the Grid is enabled
                        if self.prediction == "NOT SAFE":
                            cv2.rectangle(self.image, (x, y), (x + w, y + h), (36, 0, 255), 2)
                        elif self.prediction == "SAFE":
                            cv2.rectangle(self.image, (x, y), (x + w, y + h), (30, 255, 0), 2)

                    facess = faceCascade.detectMultiScale(roi_gray)
                    if len(facess) != 0:
                        for (ex, ey, ew, eh) in facess:
                            face_roi = roi_color[ey: ey + eh, ex:ex + ew]
                final_image = cv2.resize(face_roi, (224, 224))
                final_image = np.expand_dims(final_image, axis=0)
                final_image = final_image / 255.0 # Normalizing the data
                if time.time() - self.lastpredicted > 2:# We want to predict the result of model at every 2 seconds to avoid FPS Drop
                    self.lastpredicted = time.time()
                    threading.Thread(target=self.predict(final_image)).start()
            threading.Thread(target=self.update).start()
            key = cv2.waitKey(1) & 0xFF
            if self.started == False or self.windowIsOpened == False: ## If the button "STOP" is pressed or the window is CLOSED, then break the loop and stop the WebCam:
                break
        vid.release()
        cv2.destroyAllWindows()
    def setPhoto(self, image):

        """
        This function will take image input and resize it
        only for display purpose and convert it to QImage
        to set on the CameraPlace.
        """

        if self.PhotoSet == True: # If the STOP Button is pressed
            if self.started == False:
                self.cameraPlace.setPixmap(QtGui.QPixmap("")) # We don't want to display anything on the CameraPlace
                self.PhotoSet = False
            else:
                self.tmp = image
                image = imutils.resize(image, width=709)
                frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
                self.cameraPlace.setPixmap(QtGui.QPixmap.fromImage(image)) # Setting the real-time image of WebCam in CameraPlace

    def update(self):

            """
            This function will update the image (WebCam input) and add some indicators on it
            """

            img = self.image

            # Here we add display text to the image
            text = str(time.strftime("%H:%M %p"))
            img = ps.putBText(img, text, text_offset_x=self.image.shape[1] - 180, text_offset_y=30, vspace=20, hspace=10,
                              font_scale=1.0, background_RGB=(252, 213, 96), text_RGB=(255, 255, 255))
            text = str(self.prediction)
            if self.prediction == "SAFE":
                img = ps.putBText(img, text, text_offset_x=20, text_offset_y=30, vspace=20, hspace=10, font_scale=1.0,
                                  background_RGB=(0, 128, 0), text_RGB=(255, 255, 255))
            elif self.prediction == "NOT SAFE":
                img = ps.putBText(img, text, text_offset_x=20, text_offset_y=30, vspace=20, hspace=10, font_scale=1.0,
                                  background_RGB=(255, 0, 0), text_RGB=(255, 255, 255))
                if self.soundOn == True:
                    if time.time() - self.lastplayed > 5 and self.isThereAFace:
                        self.lastplayed = time.time()
                        threading.Thread(target=self.play).start()
            img = cv2.resize(img, (711, 501))
            threading.Thread(target=self.setPhoto(img)).start() # Calling the function to set the real-time image of WebCam in CameraPlace

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Stay Safe"))
        self.startButton.setText(_translate("MainWindow", ""))
        self.closeButton.setText(_translate("MainWindow", ""))
        self.soundButton.setText(_translate("MainWindow", ""))
        self.gridButton.setText(_translate("MainWindow", ""))


    def closeWindow(self):
        self.windowIsOpened = False # If the Close Button ("X") is pressed, we must disable the camera. Otherwise it will continue running after the close of Window
        QtCore.QCoreApplication.instance().quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet('QMainWindow{background-color: #0b6c59;border: 0px solid black;}')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

