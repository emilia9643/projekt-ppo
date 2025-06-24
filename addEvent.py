from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDateTimeEdit, QPushButton, QHBoxLayout, QTextEdit
from PyQt5.QtCore import QDateTime
from functions import qtDatetimeToDatetime as dtc

class AddEventDialog(QDialog):
    def __init__(self, tempcalendar):
        super().__init__()
        self.tempcalendar = tempcalendar
        self.setWindowTitle("Add Event")
        layout = QFormLayout()
        self.summary = QLineEdit()
        self.startdate = QDateTimeEdit()
        self.startdate.setDateTime(QDateTime.currentDateTime())
        self.enddate = QDateTimeEdit()
        self.enddate.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        self.description = QTextEdit()
        self.acceptButton = QPushButton()
        self.acceptButton.setText("y")
        self.acceptButton.setStyleSheet("width:75px;")
        self.acceptButton.clicked.connect(self.saveEvent)
        self.declineButton = QPushButton()
        self.declineButton.setText("n")
        self.declineButton.setStyleSheet("width:75px;")
        self.declineButton.clicked.connect(self.close)
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.acceptButton)
        self.button_layout.addWidget(self.declineButton)
        self.button_layout.setSpacing(5)
        self.description.setMaximumHeight(100)
        layout.addRow("Title: ", self.summary)
        layout.addRow("Start: ", self.startdate)
        layout.addRow("End: ", self.enddate)
        layout.addRow("Description: ", self.description)
        layout.addRow("", self.button_layout)
        layout.setSpacing(10)
        self.setLayout(layout)
        self.setStyleSheet("width:200px")

    def saveEvent(self):
        t1 = dtc(self.startdate)
        t2 = dtc(self.enddate)
        desc = self.description.toPlainText()
        self.tempcalendar.addEvent(self.summary.text(), t1, t2, desc)
        self.close()