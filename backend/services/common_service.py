import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile

from backend.common.config import FileConfig
from backend.common.responses import response_200, streaming_response_200, response_500
from backend.common.token import token_client
from backend.schemas.common_schema import *

app_common = APIRouter()


@app_common.post("/upload_file/{file_type}", response_model=UploadFileResp, summary='上传文件')
async def common_upload_file(file_type: str, file: UploadFile, user_id: str = Depends(token_client.token_verification)):
    try:
        # 文件名不能为空
        if not file.filename:
            raise HTTPException(status_code=400, detail='文件名不能为空')

        # 创建文件夹
        try:
            os.makedirs(os.path.join(FileConfig.path, file_type))
        except FileExistsError:
            pass

        filename = f'{str(uuid.uuid4())}-{file.filename}'
        filepath = os.path.join(FileConfig.path, file_type, filename)
        with open(filepath, 'wb') as f:
            # 流式写出大型文件，这里的10代表10MB
            for chunk in iter(lambda: file.file.read(1024 * 1024 * 10), b''):
                f.write(chunk)
    except Exception as e:
        return response_500(data="", message=str(e))

    return response_200(data={'path': os.path.join(file_type, filename)}, message='文件上传成功')


@app_common.post("/download_file", summary='下载文件')
async def common_download_file(body: DownloadFileBody, user_id: str = Depends(token_client.token_verification)):
    if not os.path.exists(os.path.join(FileConfig.path, body.path)):
        raise HTTPException(status_code=400, detail='文件不存在')
    try:
        def generate_file():
            with open(os.path.join(FileConfig.path, body.path), 'rb') as response_file:
                yield from response_file

        return streaming_response_200(data=generate_file())

    except Exception as e:
        return response_500(data="", message=str(e))
