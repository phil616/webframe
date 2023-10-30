from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Union
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette import status
from typing import Optional, Any


def E401(details: Optional[Any] = None, headers: Optional[dict[str, Any]] = None) -> None:
    # TODO log here
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=details,
        headers=headers
    )


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """
    http异常处理
    :param _:
    :param exc:
    :return:
    """
    if exc.status_code == 401:
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

    return JSONResponse({
        "code": exc.status_code,
        "message": exc.detail,
        "data": exc.detail
    }, status_code=exc.status_code, headers=exc.headers)
