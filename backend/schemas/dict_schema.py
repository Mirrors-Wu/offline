from typing import List, Optional

from pydantic import BaseModel, constr


class DictTypeCreateBody(BaseModel):
    dict_type: constr(min_length=2, max_length=20)
    notes: str


class DictTypeGetItem(BaseModel):
    dict_type_id: int
    dict_type: str
    status: int
    notes: str
    create_time: str
    create_user: str
    update_time: str
    update_user: str


class DictTypeGetResp(BaseModel):
    dict_type_list: List[DictTypeGetItem]


class DictTypeEditBody(BaseModel):
    dict_type_id: int
    dict_type: Optional[str] = None
    status: Optional[int] = None
    notes: Optional[str] = None


class DictTypeDeleteBody(BaseModel):
    dict_type_id: int
    dict_type: str


class DictDataCreateBody(BaseModel):
    dict_name: constr(min_length=2, max_length=20)
    dict_type_id: int
    dict_type: str
    dict_value: str


class DictDataGetBody(BaseModel):
    dict_type_id: int
    dict_type: str


class DictDataGetItem(BaseModel):
    dict_id: int
    dict_name: str
    dict_type_id: int
    dict_type: str
    dict_value: str
    create_time: str
    create_user: str
    update_time: str
    update_user: str


class DictDataGetResp(BaseModel):
    dict_list: List[DictDataGetItem]


class DictDataEditBody(BaseModel):
    dict_id: int
    dict_name: Optional[constr(min_length=2, max_length=20)] = None
    dict_type_id: Optional[int] = None
    dict_type: Optional[str] = None
    dict_value: Optional[str] = None


class DictDataDeleteBody(BaseModel):
    dict_id: int
    dict_name: str
