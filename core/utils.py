import os
import uuid
import hashlib
from datetime import datetime
from starlette.requests import Request
import jwt

from config import appcfg


def create_path(path: os.PathLike):
    if not os.path.exists(path):
        os.makedirs(path)


def get_path_type(path: os.PathLike):
    # 1 2 4 8 16 32 64
    result = 0b00000000
    os.path.isdir(path)
    os.path.isfile(path)
    os.path.isabs(path)
    os.path.islink(path)
    os.path.ismount(path)



def random_str(str_type=1) -> str:
    """
    生成UUID，随机字符串
    :param str_type: 4类或1类UUID
    :return:
    """
    if str_type == 2:
        only = hashlib.md5(str(uuid.uuid4()).encode(encoding='UTF-8')).hexdigest()
        return str(only)
    else:
        only = hashlib.md5(str(uuid.uuid1()).encode(encoding='UTF-8')).hexdigest()
        return str(only)


def gen_file_hash(file: bytes) -> str:
    """
    生成文件哈希
    :param file: 文件比特
    :return:
    """
    hash_obj = hashlib.sha256()
    hash_obj.update(file)
    return hash_obj.hexdigest()


def get_process_time() -> str:
    """
    获取处理时间
    只用在app启动时接收到X-Process-Time中提供时间参考
    :return:
    """
    now = datetime.now()
    time_string = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    return time_string

