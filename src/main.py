from fastapi import FastAPI, staticfiles, HTTPException
from config import appcfg
from core.events import startup, stopping
from core.exceptions import http_error_handler
from core.middlewares import BaseMiddleware
from fastapi.middleware.cors import CORSMiddleware
from endpoints.api import api_router

application = FastAPI(
    debug=appcfg.APP_DEBUG,
    title=appcfg.APP_TITLE,
    version=appcfg.APP_VERSION,
    description=appcfg.APP_DESC,
    summary=appcfg.APP_SUMMARY
)

application.add_middleware(BaseMiddleware)
application.add_middleware(
    CORSMiddleware,
    allow_origins=appcfg.CORS_ORIGINS,
    allow_credentials=appcfg.CORS_ALLOW_CREDENTIALS,
    allow_methods=appcfg.CORS_ALLOW_METHODS,
    allow_headers=appcfg.CORS_ALLOW_HEADERS,
)


application.add_exception_handler(HTTPException,http_error_handler)


application.add_event_handler("startup", startup(application))
application.add_event_handler("shutdown", stopping(application))

application.mount("/static", staticfiles.StaticFiles(directory="static"), name="static")

application.include_router(api_router)
