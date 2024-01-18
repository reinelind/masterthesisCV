from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox
import os
import shutil

class DeletePersonWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Видалити особу')
        self.setGeometry(300, 300, 300, 250)

        self.listWidget = QListWidget(self)
        self.deleteButton = QPushButton('Видалити особу', self)
        self.deleteButton.clicked.connect(self.deletePerson)
        layout = QVBoxLayout(self)
        layout.addWidget(self.listWidget)
        layout.addWidget(self.deleteButton)
        self.loadDirectory()

    def loadDirectory(self):
        self.listWidget.clear()
        base_path = './dataset'
        if os.path.exists(base_path):
            for name in os.listdir(base_path):
                path = os.path.join(base_path, name)
                if os.path.isdir(path):
                    self.listWidget.addItem(name)


    def deletePerson(self):
        selected_item = self.listWidget.currentItem()
        if selected_item is not None:
            person_name = selected_item.text()
            dir_path = os.path.join('./dataset', person_name)
            shutil.rmtree(dir_path)
            self.loadDirectory()
        else:
            QMessageBox.information(self, 'Інформація', 'Будь ласка, оберіть особу для видалення', QMessageBox.Ok)