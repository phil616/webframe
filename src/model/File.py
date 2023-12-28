from tortoise import fields
from .BaseTimestampMixin import TimestampMixin
from typing import List, Optional
from pydantic import BaseModel



class FileObject(TimestampMixin):
    fid = fields.IntField(pk=True, description='主键id')
    file_id = fields.CharField(max_length=255, null=False, description='文件唯一标识')
    file_name = fields.CharField(max_length=255, null=False, description='文件名')
    file_size = fields.IntField(null=False, description='文件大小')
    file_mime_type = fields.CharField(max_length=255, null=False, description='文件类型')
    file_info = fields.CharField(max_length=255, null=True, description='文件信息')
    file_path = fields.CharField(max_length=255, null=False, description='文件路径')
    file_OSS = fields.JSONField(null=True, description="OSS云文件对象信息")

    class Meta:
        table_description = "文件索引表"
        table = "file_list"


class FileObjectSchema(BaseModel):
    file_id: str
    file_name: str
    file_size: int
    file_mime_type: str
    file_info: Optional[str]
    file_path: str
    file_OSS: Optional[str]
