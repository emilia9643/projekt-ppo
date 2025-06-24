from PyQt5.QtCore import QDateTime
from addEvent import AddEventDialog
from functions import qtDatetimeToDatetime as dtc

class EditEventDialog(AddEventDialog):
    def __init__(self, tid, tempcalendar):
        self.id = tid
        super().__init__(tempcalendar)
        self.setWindowTitle(f"Edycja wydarzenia {self.id}")
        event = next((e for e in self.tempcalendar.eventsList if e["id"] == self.id), None)
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
        t1 = dtc(self.startdate)
        t2 = dtc(self.enddate)
        desc = self.description.toPlainText()
        for i in self.tempcalendar.eventsList:
            if i["id"] == self.id:
                i["summary"] = self.summary.text()
                i["dtstart"] = t1
                i["dtend"] = t2
                i["description"] = desc
                self.tempcalendar.save_from_list()
                self.close()
                break