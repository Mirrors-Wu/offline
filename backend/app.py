import json

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager

from common.exceptions import *
from common.init.init_dir import init_dir
from common.init.init_table import init_table
from common.logger import Logger
from common.responses import *
from services.login_service import app_login
from services.dict_service import app_dict
from services.group_service import app_group
from services.common_service import app_common
from services.activity_service import app_activity

logger = Logger(__name__)

# 初始化数据表
init_table()

app = FastAPI(
    title='offline-backend',
    description='offline-后台管理系统接口文档',
    version='0.0.1'
)

# 前端页面url
origins = [
    "http://localhost:8088",
    "http://127.0.0.1:8088",
]

# 后台api允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        content=jsonable_encoder({"message": exc.detail, "code": exc.status_code}),
        status_code=exc.status_code
    )


@app.exception_handler(AuthException)
async def auth_exception_handler(request: Request, exc: AuthException):
    return response_401(data=exc.data, message=exc.message)


# 自定义权限检验异常
@app.exception_handler(LoginException)
async def login_exception_handler(request: Request, exc: PermissionException):
    return response_400(data=exc.data, message=exc.message)


# 添加接口
app.include_router(app_login, prefix='/offline/login', tags=['登录模块'])
app.include_router(app_dict, prefix='/offline/dict', tags=['字典管理'])
app.include_router(app_group, prefix='/offline/group', tags=['社团管理'])
app.include_router(app_activity, prefix='/offline/activity', tags=['活动管理'])
app.include_router(app_common, prefix='/offline/common', tags=['通用接口'])


# ------------------------------------------
# 生成 OpenAPI 文档
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="offline小程序-后台管理系统",
        version="1.0.0",
        description="",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
# 保存 OpenAPI 文档为 JSON 文件
openapi_json = app.openapi()
with open('openapi.json', 'w', encoding='utf-8') as file:
    json.dump(openapi_json, file, ensure_ascii=False, indent=4)
# -----------------------------------------------

if __name__ == "__main__":
    uvicorn.run(app='app:app', host="0.0.0.0", port=8000)
