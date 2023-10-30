
from pydantic import BaseModel

class OAuth2ResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"