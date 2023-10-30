from fastapi import APIRouter

background_router = APIRouter(prefix="/background")

@background_router.post("/addJob")
async def SGN_backgroundAddJob():
    ...

