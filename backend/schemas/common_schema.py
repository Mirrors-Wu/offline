from typing import List, Optional

from pydantic import BaseModel, constr


class UploadFileResp(BaseModel):
    path: str

class DownloadFileBody(BaseModel):
    path: str
