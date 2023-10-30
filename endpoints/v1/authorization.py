from urllib.parse import quote

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from core.authorize import create_access_token
from core.exceptions import E401
from curd.User import LL_getUserByUsernameAndPassword, LL_getUserRoleByUserId
from schemas.authorize_schemas import OAuth2ResponseSchema

authorization_router = APIRouter(prefix="/authorization")


@authorization_router.post("/token", description="颁发用户token", name="用户授权")
async def SN_Authorization_Token(form_data: OAuth2PasswordRequestForm = Depends()):
    requested_scopes = set(form_data.scopes)
    if form_data.username and form_data.password:
        user = await LL_getUserByUsernameAndPassword(username=form_data.username, password=form_data.password)
        if not user:
            E401("Username invalid or password incorrect")
        user_scopes = await LL_getUserRoleByUserId(user.id)
        user_owned_scopes = set(user_scopes)
        # there are 3 kinds of situations:
        # rs > us (in this case, request failed)  rs = us  rs < us  (otherwise is success)
        # in this case if rs is subset of us, give user the rs, otherwise failed
        if not requested_scopes.issubset(user_owned_scopes):
            E401(f"Login failed. The scope obtained by the user [{','.join(requested_scopes)}]"
                 f" exceeds the scope owned by the user [{'.'.join(user_owned_scopes)}], please try again")
        jwt_data = {
            "usr": user.username,
            "scope": requested_scopes
        }
        jwt_token = create_access_token(data=jwt_data)
        resp = JSONResponse(OAuth2ResponseSchema(access_token=jwt_token).model_dump())
        cookie_string = quote("Bearer " + jwt_token)
        resp.set_cookie("Authorization", cookie_string)
        return resp
