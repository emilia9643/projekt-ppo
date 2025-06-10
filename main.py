from PyQt5.QtWidgets import QListWidgetItem,QMainWindow, QApplication, QDialog, QFormLayout, QLineEdit, QDateTimeEdit, QPushButton, QHBoxLayout, QTextEdit
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate, QDateTime, QTimer
from datetime import datetime
import sys
import os
import icalhandler
from functions import formattime as ft
from functions import qtDatetimeToDatetime as dtc
from tkinter import Tk, filedialog

tempcalendar=icalhandler.newCalendar("example.ics")

root=Tk()
root.withdraw()

class AddEventDialog(QDialog):
    def closeDialog(self):
        self.close()
    def saveEvent(self):
        t1=dtc(self.startdate)
        t2=dtc(self.enddate)
        desc = self.description.toPlainText()
        tempcalendar.addEvent(self.summary.text(), t1, t2, desc)
        self.close()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Event")
        layout=QFormLayout()
        self.summary=QLineEdit()
        self.startdate=QDateTimeEdit()
        self.startdate.setDate(QDate.currentDate())
        self.enddate=QDateTimeEdit()
        self.enddate.setDate(QDate.currentDate())
        self.description=QTextEdit()
        self.acceptButton=QPushButton()
        self.acceptButton.setText("y")
        self.acceptButton.setStyleSheet("width:75px;")
        self.acceptButton.clicked.connect(self.saveEvent)
        self.declineButton=QPushButton()
        self.declineButton.setText("n")
        self.declineButton.setStyleSheet("width:75px;")
        self.declineButton.clicked.connect(self.closeDialog)
        self.button_layout=QHBoxLayout()
        self.button_layout.addWidget(self.acceptButton)
        self.button_layout.addWidget(self.declineButton)
        self.button_layout.setSpacing(5) 
        self.description.setMaximumHeight(60)
        layout.addRow("Title: ", self.summary)
        layout.addRow("Start: ", self.startdate)
        layout.addRow("End: ", self.enddate)
        layout.addRow("Description: ", self.description)
        layout.addRow("",self.button_layout)
        layout.setSpacing(10)
        self.setLayout(layout)
        self.setStyleSheet("width:200px")

class EditEventDialog(AddEventDialog):
    def __init__(self, tid):
        self.id=tid
        super().__init__()
        self.setWindowTitle(f"Edycja wydarzenia {self.id}")
        event=next((e for e in tempcalendar.eventsList if e["id"]==self.id), None)
        if event:
            self.summary.setText(event["summary"] or "")
            if event["dtstart"]:
                self.startdate.setDateTime(QDateTime(event["dtstart"]))
            if event["dtend"]:
                self.enddate.setDateTime(QDateTime(event["dtend"]))
            self.description.setText(event.get("description", "") or "")  

        self.acceptButton.clicked.disconnect()
        self.acceptButton.clicked.connect(self.editEvent)

    def editEvent(self):
        t1=dtc(self.startdate)
        t2=dtc(self.enddate)
        desc = self.description.toPlainText()
        for i in tempcalendar.eventsList:
            if i["id"]==self.id:
                i["summary"]=self.summary.text()
                i["dtstart"]=t1
                i["dtend"]=t2
                i["description"]=desc  
                tempcalendar._save_from_list()
                self.close()
                break

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        ui_path=os.path.dirname(os.path.abspath(__file__))
        loadUi(os.path.join(ui_path, "untitled.ui"), self)
        self.pushButton_4.clicked.connect(self.onclick)
        self.pushButton.clicked.connect(self._changecal)
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()
        self._add_items()
        self.show()

    def update_time(self):
        now=datetime.now().strftime('%H:%M:%S')
        if datetime.now().hour==21 and datetime.now().minute==41:
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
        dialog=AddEventDialog()
        dialog.exec_()
        self._add_items()
    def showEditDialog(self, tid):
        dialog=EditEventDialog(tid)
        dialog.exec_()
        self._add_items()
    
    def _changecal(self):
        fn=filedialog.askopenfilename(
            title="Select iCalendar file",
            filetypes=[("iCalendar files", "*.ics"), ("All files", "*.*")]
        )
        if fn:
            global tempcalendar
            tempcalendar=icalhandler.newCalendar(fn)
            self._add_items()
        else:
            pass

    def _add_items(self):
        self.listWidget.clear()
        for event in tempcalendar.eventsList:
            item=QListWidgetItem()
            s=event['dtstart']
            e=event['dtend']

            if s is not None and e is not None:
                button=QPushButton(f"{event['summary']} {s.hour}:{s.minute}-{e.hour}:{e.minute} {e.day}.{e.month}.{e.year} || {event['description']}")
            else:
                button=QPushButton(f"{event['summary']} (brak daty)")
            if event.get("description"):
                button.setToolTip(event["description"])  
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4f4f4f;
                    border: 0.5px solid black;
                    border-radius: 5px;
                    padding: 5px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)
            button.clicked.connect(lambda _, tid=event["id"]: self.showEditDialog(tid))
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, button)

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=Ui()
    app.exec_()