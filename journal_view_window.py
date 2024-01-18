import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QWidget, QVBoxLayout, QTableWidget, \
    QTableWidgetItem

import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QWidget, QVBoxLayout, QTableWidget, \
    QTableWidgetItem, QMessageBox


class JournalViewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Журнал відвідувань")
        self.setGeometry(100, 100, 800, 600)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Ім'я", "Дата", "Коментар"])

        self.openButton = QPushButton("Відкрити журнал")
        self.openButton.clicked.connect(self.open_csv_file)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.openButton)

        self.setLayout(layout)

    def open_csv_file(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Виберіть файл CSV", "", "CSV Files (*.csv);;All Files (*)",
                                                  options=options)

        if filePath:
            if filePath.endswith(".csv"):
                self.load_csv_data(filePath)
            else:
                QMessageBox.critical(self, "Увага", "Ідентифіковано небажану людину:Steve_Jobs!")

    def load_csv_data(self, file_path):
        self.tableWidget.setRowCount(0)
        with open(file_path, newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row_num, row_data in enumerate(csv_reader):
                self.tableWidget.insertRow(row_num)
                for col_num, cell_data in enumerate(row_data[:2]):
                    self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(cell_data))


