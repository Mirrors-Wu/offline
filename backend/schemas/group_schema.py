from typing import List, Optional

from pydantic import BaseModel, constr


class GroupCreateBody(BaseModel):
    group_name: constr(min_length=2, max_length=20)
    group_type_id: int
    group_type: str
    profile_path: str
    photo_path: str
    group_info: str


class GroupGetItem(BaseModel):
    group_id: int
    group_name: str
    group_type_id: int
    group_type: str
    profile_path: str
    photo_path: str
    group_info: str
    create_time: str
    create_user: str
    update_time: str
    update_user: str


class GroupGetResp(BaseModel):
    group_list: List[GroupGetItem]


class GroupEditBody(BaseModel):
    group_id: int
    group_name: Optional[str]
    group_type_id: Optional[int]
    group_type: Optional[str]
    profile_path: Optional[str]
    photo_path: Optional[str]
    group_info: Optional[str]


class GroupDeleteBody(BaseModel):
    group_id: int
    group_name: str
