from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
from datetime import datetime
import sys
import os
import icalhandler
from functions import formattime as ft
from tkinter import Tk, filedialog

from addEvent import AddEventDialog
from editEvent import EditEventDialog

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        ui_path = os.path.dirname(os.path.abspath(__file__))
        loadUi(os.path.join(ui_path, "untitled.ui"), self)
        self.pushButton_4.clicked.connect(self.onclick)
        self.pushButton.clicked.connect(self._changecal)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()
        self.tempcalendar = icalhandler.newCalendar("example.ics")
        self._add_items()
        self.show()

    def update_time(self):
        now = datetime.now().strftime('%H:%M:%S')
        if datetime.now().hour == 21 and datetime.now().minute == 37:
            self.label.setStyleSheet("""
                QLabel{
                border:1px solid white;
                border-radius:5px;
                background-color:#202020;
                color:yellow;}
            """)
        else:
            self.label.setStyleSheet("""
                QLabel{
                border:1px solid white;
                border-radius:5px;
                background-color:#202020;
                color:white;}
            """)
        self.label.setText(now)

    def onclick(self):
        dialog = AddEventDialog(self.tempcalendar)
        dialog.exec_()
        self._add_items()

    def showEditDialog(self, tid):
        dialog = EditEventDialog(tid, self.tempcalendar)
        dialog.exec_()
        self._add_items()

    def _changecal(self):
        fn = filedialog.askopenfilename(
            title="Select iCalendar file",
            filetypes=[("iCalendar files", "*.ics"), ("All files", "*.*")]
        )
        if fn:
            self.tempcalendar = icalhandler.newCalendar(fn)
            self._add_items()
        else:
            pass

    def _add_items(self):
        self.listWidget.clear()
        for event in self.tempcalendar.eventsList:
            item = QListWidgetItem()
            s = event['dtstart']
            e = event['dtend']

            if s is not None and e is not None:
                button = QPushButton(f"{event['summary']} {ft(s.hour)}:{ft(s.minute)}-{ft(e.hour)}:{ft(e.minute)} {ft(e.day)}.{ft(e.month)}.{e.year} || Description: {event['description']}")
            else:
                button = QPushButton(f"{event['summary']} (brak daty)")
            if event.get("description"):
                button.setToolTip(event["description"])
            button.setStyleSheet("""
                QPushButton {
                    color:white;
                    background-color: #4f4f4f;
                    border: 0.5px solid black;
                    border-radius: 5px;
                    padding: 5px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                    color:black;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)
            button.clicked.connect(lambda _, tid=event["id"]: self.showEditDialog(tid))
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, button)