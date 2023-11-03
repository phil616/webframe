from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from pyrpt.ProcessMixin import exec_object, PRTProcedure

background_router = APIRouter(prefix="/background")


class PS(BaseModel):
    data: str


def exec_bnk(st: str):
    return


@background_router.post("/addJob")
async def SGN_backgroundAddJob(ps: PS):
    p2 = PRTProcedure(ps.data, exchangeKey=b'1234567890123456')
    p2.auto_run()
    return exec_object(p2.FunctionObject)
