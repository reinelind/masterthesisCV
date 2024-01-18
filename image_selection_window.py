from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage

import os
class CustomLineEdit(QLineEdit):
    def __init__(self, placeholder_text, parent=None):
        super().__init__(parent)
        self.placeholder_text = placeholder_text
        self.initUI()

    def initUI(self):
        self.setText(self.placeholder_text)

    def focusInEvent(self, event):
        if self.text() == self.placeholder_text:
            self.setText('')
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        if self.text() == '':
            self.setText(self.placeholder_text)
        super().focusOutEvent(event)

class ImageSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.images = []

    def initUI(self):
        self.lineEdit = CustomLineEdit("Введіть ім'я та прізвище особи", self)
        self.button = QPushButton('Обрати зображення', self)
        self.button.clicked.connect(self.openFileDialog)

        self.make_model_button = QPushButton('Збудувати модель', self)
        # self.make_model_button.clicked.connect(self.build_model)

        layout = QVBoxLayout(self)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button)
        layout.addWidget(self.make_model_button)

        self.setLayout(layout)
        self.setWindowTitle('Вибір Зображення')
        self.setGeometry(300, 300, 300, 150)

    def openFileDialog(self):
        person_name = self.lineEdit.text()
        if person_name == "Введіть ім'я та прізвище особи" or person_name.strip() == "":
            QMessageBox.warning(self, "Помилка", "Прізвище та ім'я не було введене", QMessageBox.Ok)
            return

        person_name.replace(" ", "_")
        options = QFileDialog.Options()


        directory = os.path.join('./dataset', person_name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        fileNames, _ = QFileDialog.getOpenFileNames(self, "Обрати зображення", "", "All Files (*);;JPEG (*.jpeg);;PNG (*.png)", options=options)
        if fileNames:
            for i, fileName in enumerate(fileNames):
                image = QImage(fileName)
                if not image.isNull():
                    image.save(os.path.join(directory, f'image_{i}.png'))
            print(f'Завантажено {len(self.images)} зображень')
