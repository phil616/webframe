from fastapi import APIRouter, Request
from sys import version_info
from model.User import User

resource_router = APIRouter(prefix="/resources")


@resource_router.get("/secure")
async def DN_ResourcesSecure(req: Request):
    return {"success": req.app.state.user}


@resource_router.get("/systeminfo/version")
async def SN_resourcesGetSysteminfoVersion():
    return tuple(version_info)


@resource_router.get("/get/user/info")
async def SN_resourceGetUserInfo(username: str):
    user = User.filter(username=username).all()
    return user
