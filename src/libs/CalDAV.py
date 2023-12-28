import caldav
from uuid import uuid4
from model.Calendar import ICSEvent
from datetime import date, datetime
import pytz
from config import appcfg

CalDAVClient = caldav.davclient.DAVClient(
    url=appcfg.CALDAV_SERVER,
    username=appcfg.CALDAV_USERNAME,
    password=appcfg.CALDAV_PASSWORD
)


def gen_uuid():
    return str(uuid4())


def ISO8601_now():
    return datetime.now(tz=pytz.timezone('Europe/London')).strftime("%Y%m%dT%H%M%SZ")


def ISO8601(dt: datetime):
    return dt.strftime("%Y%m%dT%H%M%SZ")


def day2dt(day: date) -> datetime:
    return datetime(day.year, day.month, day.day)


def add_day(old_date: datetime, offset: int = 1) -> datetime:
    old = old_date.timestamp()
    add = 24 * 60 * 60 + offset + old
    new = datetime.fromtimestamp(add)
    return new


def render_ics(data: ICSEvent) -> str:
    if data.all_day:
        dtstart = f"VALUE=DATE:{data.day.strftime('%Y%m%d')}"
        dtend = f"VALUE=DATE:{add_day(day2dt(data.day)).strftime('%Y%m%d')}"
    else:
        dtstart = f"TZID={appcfg.GLOBAL_TIMEZONE}:{ISO8601(data.start_time)}"
        dtend = f"TZID={appcfg.GLOBAL_TIMEZONE}:{ISO8601(data.end_time)}"
    return f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//{appcfg.CALENDAR_DOMAIN}//{appcfg.CALENDAR_NAME}//EN
BEGIN:VEVENT
SUMMARY:{data.title}
DTSTART;{dtstart}
DTEND;{dtend}
DTSTAMP:{ISO8601_now()}
UID:{data.uid}
SEQUENCE:0
DESCRIPTION:{data.describe}
LAST-MODIFIED:{ISO8601_now()}
LOCATION:{data.location}
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:Reminder
TRIGGER;VALUE=DURATION:-PT12H
END:VALARM
END:VEVENT
END:VCALENDAR
"""


def read_ics(data: str):
    """
    parse like this:
    BEGIN:VCALENDAR
        VERSION:2.0
        PRODID:-//GreenShadeCapital.com//UnionWork117//EN

        BEGIN:VEVENT
        SUMMARY:OPTION TITLE
        DTSTART;VALUE=DATE:20231101
        DTEND;VALUE=DATE:20231102
        DTSTAMP:20231030T041539Z
        UID:cf3bbb84-c404-49de-8334-835f3aa081d6
        SEQUENCE:2
        DESCRIPTION:mydesc[https://cloud.tencent.com/developer/user/6258660]
        LAST-MODIFIED:20231030T041539Z
        LOCATION:myloca[https://cloud.tencent.com/developer/user/6258660]

            BEGIN:VALARM
            ACTION:DISPLAY
            DESCRIPTION:Reminder
            TRIGGER;VALUE=DURATION:-PT12H
            END:VALARM

        END:VEVENT

    END:VCALENDAR

    :param data:
    :return:
    """
    raise NotImplementedError()


def put_ics(ics: str):
    user_calendar = None
    cals = CalDAVClient.principal().calendars()
    for c in cals:
        if c.name == appcfg.CALDAV_CALENDAR_NAME:
            user_calendar = c
            break

    r = user_calendar.add_event(ical=ics)
    return r.url
