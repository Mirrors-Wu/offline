from datetime import datetime
from typing import Any

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response, StreamingResponse


def response_200(*, data: Any = None, message="获取成功") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {
                'code': 200,
                'message': message,
                'data': data,
                'success': 'true',
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    )


def streaming_response_200(*, data: Any = None):
    return StreamingResponse(
        status_code=status.HTTP_200_OK,
        content=data,
    )


def response_400(*, data: Any = None, message: str = "获取失败") -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {
                'code': 400,
                'message': message,
                'data': data,
                'success': 'false',
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    )


def response_401(*, data: Any = None, message: str = "获取失败") -> Response:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder(
            {
                'code': 401,
                'message': message,
                'data': data,
                'success': 'false',
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    )


def response_403(*, data: Any = None, message: str = "获取失败") -> Response:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=jsonable_encoder(
            {
                'code': 403,
                'message': message,
                'data': data,
                'success': 'false',
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    )


def response_500(*, data: Any = None, message: str = "接口异常") -> Response:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(
            {
                'code': 500,
                'message': message,
                'data': data,
                'success': 'false',
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    )
