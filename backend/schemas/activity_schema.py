from typing import List, Optional

from pydantic import BaseModel, constr


class ActivityCreateBody(BaseModel):
    activity_name: str
    activity_status: int  # 活动状态 0: 未开始 1：已开始 2：已结束 3: 未发布 -1：已删除
    activity_type_id: int
    activity_type: str
    photo_path: str
    number_limit_lower: int
    number_limit_upper: int
    price: float
    region_id: int
    region: str
    group_id: int
    group_name: str
    start_time: str
    end_time: str
    register_end_time: str
    activity_info: str


class ActivityGetItem(BaseModel):
    activity_id: int
    activity_name: str
    activity_status: str
    activity_type_id: int
    activity_type: str
    photo_path: str
    number_limit_lower: int
    number_limit_upper: int
    price: float
    region_id: int
    region: str
    group_id: int
    group_name: str
    start_time: str
    end_time: str
    register_end_time: str
    activity_info: str
    create_time: str
    create_user: str
    update_time: str
    update_user: str


class ActivityGetResp(BaseModel):
    activity_list: List[ActivityGetItem]


class ActivityEditBody(BaseModel):
    activity_id: int
    activity_name: Optional[str] = None
    activity_status: Optional[str] = None
    activity_type_id: Optional[int] = None
    activity_type: Optional[str] = None
    photo_path: Optional[str] = None
    number_limit_lower: Optional[int] = None
    number_limit_upper: Optional[int] = None
    price: Optional[float] = None
    region_id: Optional[int] = None
    region: Optional[str] = None
    group_id: Optional[int] = None
    group_name: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    register_end_time: Optional[str] = None
    activity_info: Optional[str] = None


class ActivityDeleteBody(BaseModel):
    activity_id: int
    activity_name: str
