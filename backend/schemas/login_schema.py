from pydantic import BaseModel, constr, Field
from typing import Optional


class LoginBody(BaseModel):
    user_name: str = Field(..., example='admin', title='账号', description='')
    password: str = Field(..., example='123456', title='密码', description='')


class LoginResp(BaseModel):
    user_name: constr(min_length=5, max_length=20) = Field(..., example='admin', title='账号', description='')
    token: str = Field(..., example='this is a token', title='token', description='')
