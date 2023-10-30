
from urllib.parse import unquote

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from typing import Dict, Optional

from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED


class CookieSecurity(OAuth2PasswordBearer):
    def __init__(self, tokenUrl:
                str,
                 scheme_name: Optional[str] = None,
                 scopes: Optional[Dict[str, str]] = None,
                 description: Optional[str] = None,
                 auto_error: bool = True,
                 cookie_name: str = "Authorization"
                 ) -> None:
        super().__init__(
            tokenUrl,
            scheme_name,
            scopes,
            description,
            auto_error,
        )
        self.cookie_name = cookie_name

    @staticmethod
    def partition_from_cookie(cookie_str: Optional[str]) -> str:
        if not cookie_str:
            return ""
        return unquote(cookie_str)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        cookie_authorization = request.cookies.get(self.cookie_name)  # get cookie auth string

        self.cookie_auth = self.partition_from_cookie(cookie_authorization)  # parse cookie string
        scheme, param = get_authorization_scheme_param(authorization)  # spilt header WWW-

        cookie_scheme, cookie_param = get_authorization_scheme_param(self.cookie_auth)  # spilt cookie string

        if cookie_param and cookie_scheme.lower() == "bearer":
            # Authorized by Cookie
            return cookie_param
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param
