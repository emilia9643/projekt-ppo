from icalendar import Calendar, Event, vDatetime
from datetime import datetime, timezone

def _utc(dt):
    if dt is None:
        return None
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    return dt

class newCalendar:
    def __init__(self, icalpath):
        self.icalpath=icalpath
        with open(self.icalpath, 'rb') as g:
            self.gcal=Calendar.from_ical(g.read())
        self.eventsList=[]
        t_id=0
        for i in self.gcal.walk():
            if i.name=="VEVENT":
                dtstart=i.get('DTSTART')
                dtend=i.get('DTEND')
                description = i.get('DESCRIPTION')  
                if hasattr(dtstart, "dt"):
                    dtstart=dtstart.dt
                if hasattr(dtend, "dt"):
                    dtend=dtend.dt
                dtstart=_utc(dtstart)
                dtend=_utc(dtend)
                self.eventsList.append({
                    'id': t_id,
                    'summary': i.get('SUMMARY'),
                    'dtstart': dtstart,
                    'dtend': dtend,
                    'description': description  
                })
            t_id += 1
        self._sortEventsByStart()

    def addEvent(self, summary, dtstart, dtend, description=""):
        t=Event()
        t['SUMMARY']=summary
        t['DTSTART']=vDatetime(_utc(dtstart))
        t['DTEND']=vDatetime(_utc(dtend))
        if description:
            t['DESCRIPTION'] = description
        self.gcal.add_component(t)
        self._save_calendar()
        self._reload_events_list()

    def _sortEventsByStart(self):
        self.eventsList.sort(key=lambda event: event['dtstart'] if event['dtstart'] is not None else datetime.min.replace(tzinfo=timezone.utc))

    def _reload_events_list(self):
        self.eventsList=[]
        t_id=0
        for i in self.gcal.walk():
            if i.name=="VEVENT":
                dtstart=i.get('DTSTART')
                dtend=i.get('DTEND')
                description = i.get('DESCRIPTION')  
                if hasattr(dtstart, "dt"):
                    dtstart=dtstart.dt
                if hasattr(dtend, "dt"):
                    dtend=dtend.dt
                dtstart=_utc(dtstart)
                dtend=_utc(dtend)
                self.eventsList.append({
                    'id': t_id,
                    'summary': i.get('SUMMARY'),
                    'dtstart': dtstart,
                    'dtend': dtend,
                    'description': description  
                })
            t_id += 1
        self._sortEventsByStart()

    def _save_calendar(self):
        with open(self.icalpath, 'wb') as file:
            file.write(self.gcal.to_ical())

    def save_from_list(self):
        self.gcal.subcomponents=[c for c in self.gcal.subcomponents if getattr(c, "name", "") != "VEVENT"]
        for i in self.eventsList:
            t=Event()
            t['SUMMARY']=i["summary"]
            if i["dtstart"] is not None:
                t['DTSTART']=vDatetime(_utc(i["dtstart"]))
            if i["dtend"] is not None:
                t['DTEND']=vDatetime(_utc(i["dtend"]))
            if i.get("description"):
                t['DESCRIPTION'] = i["description"]
            self.gcal.add_component(t)
        self._save_calendar()
        self._reload_events_list()