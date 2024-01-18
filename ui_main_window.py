from PyQt5 import QtCore, QtGui, QtWidgets
from image_selection_window import ImageSelectionWindow
from delete_person_window import DeletePersonWindow
from journal_view_window import JournalViewWindow
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 400)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.image_label = QtWidgets.QLabel(Form)
        self.image_label.setObjectName("image_label")
        self.verticalLayout.addWidget(self.image_label)
        self.control_bt = QtWidgets.QPushButton(Form)
        self.control_bt.setObjectName("control_bt")
        self.add_student_bt = QtWidgets.QPushButton(Form)
        self.add_student_bt.setObjectName("add_student_bt")
        self.delete_student_bt = QtWidgets.QPushButton(Form)
        self.delete_student_bt.setObjectName("delete_student_bt")
        self.show_journal_bt = QtWidgets.QPushButton(Form)
        self.show_journal_bt.setObjectName("show_journal")
        self.verticalLayout.addWidget(self.control_bt)
        self.verticalLayout.addWidget(self.add_student_bt)
        self.verticalLayout.addWidget(self.delete_student_bt)
        self.verticalLayout.addWidget(self.show_journal_bt)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.retranslateUi(Form)

        self.add_student_bt.clicked.connect(self.openImageSelectionWindow)
        self.delete_student_bt.clicked.connect(self.openDeleteImageWindow)
        self.show_journal_bt.clicked.connect(self.openJournalViewWindow)
        QtCore.QMetaObject.connectSlotsByName(Form)



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Cam view"))
        self.image_label.setText(_translate("Form", "TextLabel"))
        self.control_bt.setText(_translate("Form", "Старт"))
        self.add_student_bt.setText(_translate("Form", "Додати особу"))
        self.delete_student_bt.setText(_translate("Form", "Видалити особу"))
        self.show_journal_bt.setText(_translate("Form", "Показати журнал відвідувань"))

    def openImageSelectionWindow(self):
        self.image_selection_window = ImageSelectionWindow()
        self.image_selection_window.show()

    def openDeleteImageWindow(self):
        self.delete_image_window = DeletePersonWindow()
        self.delete_image_window.show()

    def openJournalViewWindow(self):
        self.journal_view_window = JournalViewWindow()
        self.journal_view_window.show()