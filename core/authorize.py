from datetime import timedelta, datetime
from enum import Enum
from typing import Union, List

import jwt
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from fastapi.security import APIKeyCookie
from fastapi import Depends, Cookie
from pydantic import ValidationError
from starlette.requests import Request, http_cookies, cookie_parser
from config import appcfg
from core.exceptions import E401
from core.runtime import syslog
from core.security import CookieSecurity


def create_access_token(data: dict) -> str:
    """
    返回JWT的token字符串
    :param data: 负载数据
    :return: 负载数据被转换后的字符串
    """
    token_data = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=appcfg.JWT_ACCESS_EXPIRE_MINUTES)  # JWT过期分钟
    token_data.update({"exp": expire})
    jwt_token = jwt.encode(token_data, appcfg.JWT_SECRET_KEY, algorithm=appcfg.JWT_ALGORITHM)  # 加入token
    return jwt_token


user_scopes = {
    "admin": "administrator of system",
    "user": "current user",
    "system": "system admin"
}

OAuth2 = CookieSecurity("/authorization/token", scopes=user_scopes)


class UserRoleMapping(Enum):
    # just for visual alignment
    user = 0b0000000001
    admin = 0b000000010
    management = 0b0100
    system = 0b00001000


def DOC_generate_mapping_doc():
    max_role = 0
    for i in UserRoleMapping:
        if i.value > max_role:
            max_role = i.value
    max_role = max_role << 1
    doc_str = ""
    _ = []
    for n in range(max_role + 1):
        for scope in UserRoleMapping:
            if n & scope.value:
                _.append(scope.name)
        doc_str += f"When IntNumber is {n} (BIN={bin(n)}, mapping the scope {_})\n"
        _.clear()
    return doc_str


def scope_mapping(scope_number: int) -> List[str]:
    scopes = []
    for scope in UserRoleMapping:
        if scope_number & scope.value:
            scopes.append(scope.name)
    return scopes


async def check_permissions(required_scope: SecurityScopes, token=Depends(OAuth2)):
    payload = None
    try:
        payload = jwt.decode(token, appcfg.JWT_SECRET_KEY, algorithms=[appcfg.JWT_ALGORITHM])
        if not payload:
            E401("Invalid certification", {"WWW-Authenticate": f"Bearer {token}"})
    except jwt.ExpiredSignatureError:
        E401("Certification has expired", {"WWW-Authenticate": f"Bearer {token}"})
    except jwt.InvalidTokenError:
        E401("Certification parse error", {"WWW-Authenticate": f"Bearer {token}"})
    except (jwt.PyJWTError, ValidationError):
        E401("Certification parse failed", {"WWW-Authenticate": f"Bearer {token}"})
    user_requested_scope = payload.get("scope")
    if not set(user_requested_scope).issubset(set(required_scope.scopes)):
        E401("Not enough scope for authorization", {"WWW-Authenticate": f"Bearer {token}"})
