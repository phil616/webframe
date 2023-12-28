

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config import appcfg


async def register_mysql(app: FastAPI):
    """
    注册mysql数据库，自动建表，从config中读取信息
    :param app:
    :return:
    """
    register_tortoise(
        app,
        config=appcfg.DB_ORM_CONFIG,
        generate_schemas=appcfg.MYSQL_TABLE_AUTOGEN,
        add_exception_handlers=False,
    )
