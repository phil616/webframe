from fastapi import APIRouter

from libs.CalDAV import render_ics, put_ics
from fastapi.background import BackgroundTasks
from model.Calendar import ICSEvent, Events
from datetime import date
from core.runtime import syslog
schedule_router = APIRouter(prefix="/schedule")


async def sync_to_server(ics: ICSEvent) -> str:
    ics_text = render_ics(ics)
    url = put_ics(ics_text)
    event = await Events.filter(uid=ics.uid).first()
    event.url = url
    await event.save()
    syslog.info(f"Event(id={event.id}) send to server with URL {url}")
    return url


@schedule_router.post("/put/event")
async def NF_schedulerPutEvent(ics: ICSEvent, bkt: BackgroundTasks):
    event = await Events.create(**ics.model_dump())
    bkt.add_task(sync_to_server, ics)
    return event.id


@schedule_router.get("/get/events")
async def NF_schedulerGetEvents(userid: int):
    events = await Events.filter(user_id=userid).all()
    return events


@schedule_router.get("/get/schedule/username/{userId}/date/{scheduleDate}}")
async def NF_schedulerGetScheduleByUserAndDate(userId: int, scheduleDate: date):
    events = await Events.filter(user_id=userId).all()
    res = []
    for event in events:
        if event.day == scheduleDate:
            res.append(event)
    return res
