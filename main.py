import sys

# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import pickle
from sklearn.preprocessing import LabelEncoder
import numpy as np
import tensorflow as tf
from datetime import datetime

from keras_facenet import FaceNet

# import Opencv module
import cv2 as cv
import csv

from ui_main_window import *

class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.controlTimer)

        self.facenet = FaceNet()  # initialize_facenet
        self.faces_embeddings = np.load("faces_embeddings_done.npz")

        self.Y = self.faces_embeddings['arr_1']

        self.encoder = LabelEncoder()
        self.encoder.fit(self.Y)
        self.haarcascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.model = pickle.load(open("svm_model_160x160.pkl", 'rb'))

        current_time = datetime.now()
        self.filename = f"Zvit_{current_time.strftime('%d%m%Y')}_{current_time.strftime('%H_%M_%S')}.csv"


    # view camera
    def viewCam(self):
        # read image in BGR format
        ret, image = self.cap.read()
        # convert image to RGB format
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        gray_img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        faces = self.haarcascade.detectMultiScale(gray_img, 1.3, 5)
        for x, y, w, h in faces:
            img = image[y:y + h, x:x + w]
            img = cv.resize(img, (160, 160))
            img = np.expand_dims(img, axis=0)
            ypred = self.facenet.embeddings(img)
            unknown_person = False
            face_recognized = 0

            face_name = self.model.predict(ypred)
            probability = self.model.predict_proba(ypred)[0]
            prob_per_class_dictionary = dict(zip(self.model.classes_, probability))
            print(prob_per_class_dictionary[face_name[0]])

            for face, probability in prob_per_class_dictionary.items():
                if probability > 0.8:
                    face_recognized += 1

            if face_recognized == 0:
                final_name = 'unknown person'
            else:
                final_name = self.encoder.inverse_transform(face_name)
                try:
                    with open(self.filename.strip(), 'r') as file:
                        if final_name[0] not in file.read():
                            with open(self.filename.strip(), 'a', newline='', encoding='utf-8') as file_to_write:
                                current_time = datetime.now()
                                writer = csv.writer(file_to_write)
                                writer.writerow([final_name[0], current_time.strftime('%H:%M:%S')])
                except FileNotFoundError:
                        open(self.filename.strip(), 'w')

            cv.rectangle(image, (x, y), (x + w, y + h), (255, 0, 255), 10)
            cv.putText(image, str(final_name), (x, y - 10), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1,
                       cv.LINE_AA)
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv.VideoCapture(0)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.control_bt.setText("Стоп")
            current_time = datetime.now()
            filename = f"Звіт-{current_time.strftime('%d-%m-%Y')}-{current_time.strftime('%H:%M:%S')}.csv"


        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.control_bt.setText("Start")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())