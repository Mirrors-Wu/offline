from fastapi import APIRouter

from backend.common.crypt import crypt_client
from backend.common.exceptions import LoginException
from backend.common.postgres import pg_client
from backend.common.token import token_client
from backend.schemas.login_schema import *

app_login = APIRouter()


@app_login.post("/login_by_account", response_model=LoginResp, summary='用户登录')
async def app_login_login_by_account(body: LoginBody):
    # 查询用户是否存在
    sql_query_user = """
        SELECT password
        FROM public.dim_role
        WHERE user_name = %(user_name)s
        """
    rows = pg_client.execute_select(sql_query_user, {'user_name': body.user_name})
    if not rows:
        raise LoginException(data='', message='用户不存在')

    # 校验密码
    hash_passwd = rows[0][0]
    if not crypt_client.verify_passwd(body.password, hash_passwd):
        raise LoginException(data='', message='密码错误')

    # 生成token
    token = token_client.token_generation(body.user_name)

    return {'user_name': body.user_name, 'token': token}
