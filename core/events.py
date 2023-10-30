"""
    core.events.py
    ~~~~~~~~~
    启动逻辑，注册服务 和 必要文件结构
    :copyright: (c) 2023 by Fei Dongxu.
    :date: 2023.07.04
    :license: Apache Licence 2.0
"""
from typing import Callable
from libs.EmailServer import email_sender
from aioredis import Redis
from fastapi import FastAPI
from core.runtime import runtime_info
from databases.mysql import register_mysql
from databases.redis import sys_cache, code_cache
from core.background import generate_background_scheduler
from contextlib import asynccontextmanager
from core.runtime import syslog

schedule_dispatch = generate_background_scheduler()


def system_status_report(appinfo):
    syslog.info(f"System({appinfo}) interval background running fully operational")


def startup(app: FastAPI) -> Callable:
    """
    FastApi startup event, before application start up
    :param app: FastAPI
    :return: start_app
    """

    async def app_start() -> None:
        syslog.debug("system startup")
        app.state.cache = await sys_cache()
        app.state.code = await code_cache()
        schedule_dispatch.add_job(
            system_status_report, 'cron', name="system_status_report",
            args=[app.openapi().get("info")],
            hour=20, minute=59, second=0
        )
        schedule_dispatch.start()
        await register_mysql(app)


    return app_start


def stopping(app: FastAPI) -> Callable:
    """
    FastApi shutdown event, call when application shutting down
    :param app: FastAPI
    :return: stop_app
    """

    async def stop_app() -> None:
        # 如果想使用cache，需要在处理函数中加入req:Request
        # 并且使用req.app.state.cache来调用set和get
        cache: Redis = await app.state.cache
        code: Redis = await app.state.code
        await cache.close()
        await code.close()
        jobs = schedule_dispatch.get_jobs()
        for job in jobs:
            if job.name == "system_status_report":
                job.remove()

    return stop_app


async def runtime_test_inject_func():
    syslog.debug("test function successfully update")
    ...


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """
    the lifespan and startup/shutdown event cannot coexist in the same application
    :param app:
    :return:
    """
    runtime_info["test"] = runtime_test_inject_func
    syslog.debug(f"{app.openapi().get('info')}'s lifespan startup with a model: {runtime_info}")
    #  如果使用了Lifespan的话，就不能使用event了，yield前面是启动前的内容
    yield
    runtime_info.clear()
    syslog.debug("runtime info clean up")
