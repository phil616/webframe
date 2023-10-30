from pydantic import BaseModel
from datetime import date, datetime
from .BaseTimestampMixin import TimestampMixin
from tortoise import fields


class Events(TimestampMixin):
    id = fields.IntField(pk=True)
    user_id = fields.IntField(description="所属用户")
    title = fields.CharField(max_length=255,description="标题")
    uid = fields.CharField(max_length=255, unique=True, description="事件的UID")
    time_zone = fields.CharField(max_length=255, default="Asia/Shanghai", description="时区")
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField()
    all_day = fields.BooleanField(default=True)
    day = fields.DateField()
    location = fields.CharField(max_length=255, default="绿荫集团", description="地址")
    describe = fields.CharField(max_length=255, description="描述")
    url = fields.CharField(null=True, max_length=255, description="ICS文件URL")
    class Meta:
        table_description = "事件表"
        table = "events"


class ICSEvent(BaseModel):
    user_id: int
    uid: str
    title: str
    time_zone: str = "Asia/Shanghai"
    start_time: datetime
    end_time: datetime
    all_day: bool = True
    day: date
    location: str = "绿荫集团"
    describe: str
