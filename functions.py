from datetime import datetime

def formattime(time):
    if len(str(time))==1:
        return f"0{time}"
    else:
        return time

def qtDatetimeToDatetime(qt_datetime):
    year=qt_datetime.date().year()
    month=qt_datetime.date().month()
    day=qt_datetime.date().day()
    hour=qt_datetime.time().hour()
    minute=qt_datetime.time().minute()
    second=qt_datetime.time().second()
    py_datetime=datetime(year, month, day, hour, minute, second)
    return py_datetime