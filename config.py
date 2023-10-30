from pydantic import BaseModel
from os import path, walk
from typing import List
from os import environ


def get_models():
    skip_files = ['BaseTimestampMixin.py', '__init__.py']
    ret = []
    for _, _, i in walk(path.join("model")):
        models = list(set(i) - set(skip_files))
        for model in models:
            model = model.replace(".py", "")
            model = "model." + model
            ret.append(model)
        break
    return ret


class Config(BaseModel):
    GLOBAL_TIMEZONE: str = 'Asia/Shanghai'
    # FastAPI debug mode
    APP_DEBUG: bool = True
    APP_TITLE: str = "FastAPI General Framework"
    APP_SUMMARY: str = ""
    APP_DESC: str = ""
    APP_VERSION: str = "0.0.1"
    # Cross-Origin Resource Sharing
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]

    # JWT (Json Web Token) 
    JWT_SECRET_KEY: str = environ.get("JWT_SECRET_KEY", "rundowmkey")
    JWT_ALGORITHM: str = environ.get("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_EXPIRE_MINUTES: int = int(environ.get("JWT_ACCESS_EXPIRE_MINUTES", 24 * 60))

    # ------------------ Email server  ---------
    EMAIL_USERNAME: str = environ.get("EMAIL_USERNAME")
    EMAIL_PASSWORD: str = environ.get("EMAIL_PASSWORD")
    EMAIL_HOST_SERVER: str = environ.get("EMAIL_HOST_SERVER", "smtp.163.com")

    # ------------------ MySQL  -----------
    db_host: str = environ.get("DB_HOST", "localhost")
    db_port: int = environ.get("DB_PORT", 3306)
    db_name: str = environ.get("DB_NAME", "fastapi")
    db_user: str = environ.get("DB_USER", "root")
    db_password: str = environ.get("DB_PASSWORD", "123456")

    DB_ORM_CONFIG: dict = {
        "connections": {
            "base": {  # base database named base
                'engine': 'tortoise.backends.mysql',
                "credentials": {
                    'host': db_host,
                    'user': db_user,
                    'password': db_password,
                    'port': db_port,
                    'database': db_name,  # name of mysql database server
                }
            },
        },
        "apps": {
            "base": {
                "models": get_models(),  # model file in ./models
                "default_connection": "base"  # link to `base` database
            },
        },
        'use_tz': False,
        'timezone': GLOBAL_TIMEZONE
    }
    MYSQL_TABLE_AUTOGEN: bool = True

    # -----------------Redis-----------
    cache_host: str = environ.get("CACHE_HOST", "127.0.0.1")
    cache_port: int = environ.get("CACHE_PORT", 6379)
    CACHE_CONFIG: dict = {
        "CACHE_HOST": cache_host,  # Redis连接
        "CACHE_PORT": cache_port,  # Redis端口
        "CACHE_CP": "utf-8",  # Redis CodePage （编码）
        "CACHE_decode_responses": True  # 与Redis的连接编码，True会将结果返回为字符串
    }
    CACHE_URL: str = f"redis://{CACHE_CONFIG['CACHE_HOST']}:{CACHE_CONFIG['CACHE_PORT']}"
    CACHE_DB_IDX: dict = {
        "system": 0,
        "bin": 1,
        "log": 2,
        "access": 3,
        "info": 4,
        "doc": 5
    }

    # -------------SchedulerJobStore-----------
    # MySQL for default and python3 only
    JOB_STORE_NAME: str = "job"
    MYSQL_JOB_STORE_URL: str = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{JOB_STORE_NAME}?charset=utf8mb4'
    # -------------Disk Storage----------------
    SINGLE_FILE_STORAGE_PATH: List = [".", "storage", "single"]
    META_FILE_STORAGE_PATH: List = [".", "storage", "meta"]

    # -------------OSS Config -----------------
    OSS_ACCESS_KEY: str = environ.get("OSS_ACCESS_KEY")
    OSS_ACCESS_SECRET: str = environ.get("OSS_ACCESS_SECRET")

    # -------------App Encryption Config --------------------
    APP_ENCRYPT_SECRET: str = environ.get("APP_ENCRYPT_SECRET","APP_ENCRYPT_SECRET")  # BCrypt hash
    APP_INIT_SECRET: str = environ.get("APP_INIT_SECRET","APP_ENCRYPT_SECRET")  # INIT User

    # -------------Calendar Config -------------
    CALENDAR_NAME: str = "UnionWork"
    CALENDAR_DOMAIN: str = "Default.UnionWork"
    CALDAV_SERVER: str = environ.get("CALDAV_SERVER")
    CALDAV_USERNAME: str = environ.get("CALDAV_USERNAME")
    CALDAV_PASSWORD: str = environ.get("CALDAV_PASSWORD")
    CALDAV_CALENDAR_NAME:str = environ.get("CALDAV_CALENDAR_NAME")
    CALDAV_AUTH: str = "Basic"


appcfg = Config()
