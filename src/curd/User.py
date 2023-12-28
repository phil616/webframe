from typing import List, Union

from core.authorize import scope_mapping
from libs.crypto import cryptor
from model.User import User, UserRole


async def LL_getUserByUsername(username: str) -> User:
    user = await User.filter(username=username).first()
    return user


async def LL_getUserRoleByUserId(userid: int) -> List[str]:
    role = await UserRole.filter(userid=userid).first()
    return scope_mapping(role.user_role)


async def LL_getUserByUsernameAndPassword(username: str, password: str) -> Union[None, User]:
    user = await User.filter(username=username).first()
    if not User:
        return None
    if cryptor.verify_b(password, user.password):
        return user
    else:
        return None
