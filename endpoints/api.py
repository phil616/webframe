from core.authorize import check_permissions
from .v1 import authorization
from .v1 import resources
from fastapi import APIRouter,Security
api_router = APIRouter()

api_router.include_router(authorization.authorization_router)
api_router.include_router(resources.resource_router, dependencies=[Security(check_permissions,scopes=['admin'])])