import os
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from backend.common.config import FileConfig
from backend.common.postgres import pg_client
from backend.common.responses import response_200
from backend.common.token import token_client
from backend.schemas.group_schema import *

app_group = APIRouter()


@app_group.post("/create", summary='创建社团')
async def group_create(body: GroupCreateBody, user_id: str = Depends(token_client.token_verification)):
    # 社团是否已存在
    sql_check_group = """
    SELECT *
    FROM public.dim_group
    WHERE group_name = %(group_name)s
    """
    if pg_client.execute_select(sql_check_group, {'group_name': body.group_name}):
        raise HTTPException(status_code=400, detail=f'社团【{body.group_name}】已存在')

    # 社团类型是否已存在
    sql_check_dict = """
    SELECT *
    FROM public.dim_dict_data
    WHERE dict_id = %(group_type_id)s
    AND dict_name = %(group_type)s
    """
    if not pg_client.execute_select(sql_check_dict, {'group_type_id': body.group_type_id, 'group_type': body.group_type}):
        raise HTTPException(status_code=400, detail=f'社团类型【{body.group_type}】不存在')

    # 图片是否已成功上传
    if not os.path.exists(os.path.join(FileConfig.path, body.photo_path)):
        raise HTTPException(status_code=400, detail=f'社团图片未上传成功')
    if not os.path.exists(os.path.join(FileConfig.path, body.profile_path)):
        raise HTTPException(status_code=400, detail=f'社团头像未上传成功')

    # 创建社团
    sql_insert = """
        INSERT INTO public.dim_group
        (group_name
        ,group_type_id
        ,group_type
        ,profile_path
        ,photo_path
        ,group_info
        ,create_time
        ,create_user
        ,update_time
        ,update_user)
        VALUES (%(group_name)s
                ,%(group_type_id)s
                ,%(group_type)s
                ,%(profile_path)s
                ,%(photo_path)s
                ,%(group_info)s
                ,%(create_time)s
                ,%(create_user)s
                ,%(update_time)s
                ,%(update_user)s)
        """
    params = {
        'group_name': body.group_name,
        'group_type_id': body.group_type_id,
        'group_type': body.group_type,
        'profile_path': body.profile_path,
        'photo_path': body.photo_path,
        'group_info': body.group_info,
        'create_time': datetime.now(),
        'create_user': user_id,
        'update_time': datetime.now(),
        'update_user': user_id,
    }
    pg_client.execute_commit(sql_insert, params)

    return response_200(data='', message='社团创建成功')


@app_group.post('/get', response_model=GroupGetResp, summary='获取社团信息')
async def group_get(user_id: str = Depends(token_client.token_verification)):
    sql_get = """
    SELECT 
       group_id,
       group_name,
       group_type_id,
       group_type,
       profile_path,
       photo_path,
       group_info,
       TO_CHAR(create_time, 'YYYY-MM-DD HH24:MI:SS'),
       create_user,
       TO_CHAR(update_time, 'YYYY-MM-DD HH24:MI:SS'),
       update_user
    FROM public.dim_group
    """
    rows = pg_client.execute_select(sql_get)

    return response_200(data={
        'activity_list': [{
            'group_id': i[0],
            'group_name': i[1],
            'group_type_id': i[2],
            'group_type': i[3],
            'profile_path': i[4],
            'photo_path': i[5],
            'group_info': i[6],
            'create_time': i[7],
            'create_user': i[8],
            'update_time': i[9],
            'update_user': i[10],
        }
            for i in rows
        ]})


@app_group.post("edit", summary='修改社团信息')
async def group_edit(body: GroupEditBody, user_id: str = Depends(token_client.token_verification)):
    # TODO 社团类型校验
    set_sql = ''
    if body.group_name:
        set_sql += 'group_name = %(group_name)s,'
    if body.group_type_id and body.group_type:
        set_sql += 'group_type_id = %(group_type_id)s, group_type = %(group_type)s,'
    if body.group_info:
        set_sql += 'group_info = %(group_info)s,'
    if body.photo_path:
        # TODO 文件上传校验
        set_sql += 'photo_path = %(photo_path)s,'
    if body.profile_path:
        set_sql += 'profile_path = %(profile_path)s,'

    if not set_sql:
        return response_200(message='社团信息修改成功')

    set_sql += 'update_time = %(update_time)s, update_user = %(update_user)s'

    sql_update = f"""
    UPDATE public.dim_group
        SET {set_sql}
        WHERE group_id = %(group_id)s
    """
    params = {
        'group_id': body.group_id,
        'group_name': body.group_name,
        'group_type_id': body.group_type_id,
        'group_type': body.group_type,
        'profile_path': body.profile_path,
        'photo_path': body.photo_path,
        'group_info': body.group_info,
        'update_time': datetime.now(),
        'update_user': user_id,
    }
    pg_client.execute_commit(sql_update, params)
    return response_200(message='社团信息修改成功')


@app_group.post("delete", summary='删除社团')
async def group_delete(body: GroupDeleteBody, user_id: str = Depends(token_client.token_verification)):
    # TODO 当前有活动的社团不能删除
    sql_delete = """
    DELETE FROM public.dim_group
    WHERE group_id = %(group_id)s AND group_name = %(group_name)s
    """
    params = {
        'group_id': body.group_id,
        'group_name': body.group_name
    }
    pg_client.execute_commit(sql_delete, params)

    return response_200(message=f'社团【{body.group_name}】删除成功')
