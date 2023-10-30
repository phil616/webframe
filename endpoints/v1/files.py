
import os
from fastapi import APIRouter, UploadFile
from pydantic import BaseModel
from starlette.responses import FileResponse

from config import appcfg
from core.exceptions import E401
from core.utils import random_str
from core.persistence import write_to_path
from model.File import FileObjectSchema, FileObject

upload_route = APIRouter()

class FileStorageResp(BaseModel):
    file_id: str
    file_name: str


@upload_route.post("/new/upload/file",
                   description="文件上传接口",
                   name="文件上传")
async def SRT_upload_new_file(file: UploadFile):
    """
    上传普通文件，任何形式
    :param file: 文件bytes
    :return:
    """
    fileBytes = await file.read()
    file.file.seek(0, 2)
    fileId = random_str()
    filePath = os.path.join(*appcfg.SINGLE_FILE_STORAGE_PATH, fileId)
    file_obj = FileObjectSchema(file_id=fileId,
                                file_name=file.filename,
                                file_size=file.file.tell(),
                                file_mime_type=file.content_type,
                                file_path=filePath,
                                )
    await write_to_path(fileBytes, filePath)
    await FileObject.create(**file_obj.dict())
    resp = FileStorageResp(file_id=fileId, file_name=file.filename)
    return resp


def abstract_file_transmit(file: FileObject):
    """
    抽象文件传递
    :param file:
    :return:
    """
    filePath = file.file_path
    fileName = file.file_name
    fileType = file.file_mime_type
    return FileResponse(filePath, media_type=fileType, filename=fileName)


@upload_route.get("/get/download/uid",
                  description="文件下载接口",
                  name="文件下载")
async def SRT_download_file_by_uid(uid: str):
    file = await FileObject.filter(file_id=uid).first()
    if file is None:
        E401("未查询到文件")
    return abstract_file_transmit(file)

@upload_route.get('/get/download/filelist')
async def SRT_GET_Download_FileList():
    orm_file_list = await FileObject.all()
    file_list = []
    for file in orm_file_list:
        file_list.append(FileObjectSchema(**file.__dict__))
    return file_list
