import datetime
from enum import Enum
import caldav
import icalendar
import uuid
from model.Calendar import ICSEvent
from libs.CalDAV import read_ics, render_ics


class AliyunStorageError(Exception):
    def __init__(self, value):
        self.v = value

    def __str__(self):
        return repr(self.v)


