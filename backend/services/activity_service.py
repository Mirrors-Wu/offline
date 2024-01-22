import os
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from backend.common.config import FileConfig
from backend.common.postgres import pg_client
from backend.common.responses import response_200
from backend.common.token import token_client
from backend.schemas.activity_schema import *

app_activity = APIRouter()


@app_activity.post("/create", summary='创建活动')
async def activity_create(body: ActivityCreateBody, user_id: str = Depends(token_client.token_verification)):
    # TODO 社团校验 活动类型校验
    # TODO 活动重复校验
    # 图片是否已成功上传
    if not os.path.exists(os.path.join(FileConfig.path, body.photo_path)):
        raise HTTPException(status_code=400, detail=f'活动图片未上传成功')

    sql_insert = """
            INSERT INTO public.dim_activity
            (
            activity_name
            ,activity_status
            ,activity_type_id
            ,activity_type
            ,photo_path
            ,number_limit_lower
            ,number_limit_upper
            ,price
            ,region_id
            ,region
            ,group_id
            ,group_name
            ,start_time
            ,end_time
            ,register_end_time
            ,activity_info
            ,create_time
            ,create_user
            ,update_time
            ,update_user
            )
            VALUES (
                    %(activity_name)s
                    ,%(activity_status)s
                    ,%(activity_type_id)s
                    ,%(activity_type)s
                    ,%(photo_path)s
                    ,%(number_limit_lower)s
                    ,%(number_limit_upper)s
                    ,%(price)s
                    ,%(region_id)s
                    ,%(region)s
                    ,%(group_id)s
                    ,%(group_name)s
                    ,%(start_time)s
                    ,%(end_time)s
                    ,%(register_end_time)s
                    ,%(activity_info)s
                    ,%(create_time)s
                    ,%(create_user)s
                    ,%(update_time)s
                    ,%(update_user)s
            )
            """
    params = {
        'activity_name': body.activity_name,
        'activity_status': body.activity_status,
        'activity_type_id': body.activity_type_id,
        'activity_type': body.activity_type,
        'photo_path': body.photo_path,
        'number_limit_lower': body.number_limit_lower,
        'number_limit_upper': body.number_limit_upper,
        'price': body.price,
        'region_id': body.region_id,
        'region': body.region,
        'group_id': body.group_id,
        'group_name': body.group_name,
        'start_time': body.start_time,
        'end_time': body.end_time,
        'register_end_time': body.register_end_time,
        'activity_info': body.activity_info,
        'create_time': datetime.now(),
        'create_user': user_id,
        'update_time': datetime.now(),
        'update_user': user_id,
    }
    pg_client.execute_commit(sql_insert, params)

    return response_200(data='', message='活动创建成功')


@app_activity.post("/get", response_model=ActivityGetResp, summary='获取活动')
async def activity_get(user_id: str = Depends(token_client.token_verification)):
    # TODO 根据时间更新活动状态
    sql_get = """
        SELECT 
           activity_id,
            activity_name,
            activity_status,
            activity_type_id,
            activity_type,
            photo_path,
            number_limit_lower,
            number_limit_upper,
            price,
            region_id,
            region,
            group_id,
            group_name,
            start_time,
            end_time,
            register_end_time,
            activity_info,
           TO_CHAR(create_time, 'YYYY-MM-DD HH24:MI:SS'),
           create_user,
           TO_CHAR(update_time, 'YYYY-MM-DD HH24:MI:SS'),
           update_user
        FROM public.dim_activity
        """
    rows = pg_client.execute_select(sql_get)

    return response_200(data={
        'activity_list': [{
            'activity_id': i[0],
            'activity_name': i[1],
            'activity_status': i[2],
            'activity_type_id': i[3],
            'activity_type': i[4],
            'photo_path': i[5],
            'number_limit_lower': i[6],
            'number_limit_upper': i[7],
            'price': i[8],
            'region_id': i[9],
            'region': i[10],
            'group_id': i[11],
            'group_name': i[12],
            'start_time': i[13],
            'end_time': i[14],
            'register_end_time': i[15],
            'activity_info': i[16],
            'create_time': i[17],
            'create_user': i[18],
            'update_time': i[19],
            'update_user': i[20],
        }
            for i in rows
        ]})


@app_activity.post("edit", summary='修改活动信息')
async def activity_edit(body: ActivityEditBody, user_id: str = Depends(token_client.token_verification)):
    set_sql = ''
    for field in ['activity_name', 'activity_status', 'activity_type_id', 'activity_type', 'photo_path',
                  'number_limit_lower', 'number_limit_upper', 'price', 'region_id', 'region', 'group_id',
                  'group_name', 'start_time', 'end_time', 'register_end_time', 'activity_info']:
        if body.__getattribute__(field):
            set_sql += f'{field} = %({field})s,'

    if not set_sql:
        raise HTTPException(status_code=400, detail='修改信息不能为空')

    set_sql += 'update_time = %(update_time)s, update_user = %(update_user)s'

    sql_update = f"""
    UPDATE public.dim_activity
        SET {set_sql}
        WHERE activity_id = %(activity_id)s
    """
    params = {
        'activity_id': body.activity_id,
        'activity_name': body.activity_name,
        'activity_status': body.activity_status,
        'activity_type_id': body.activity_type_id,
        'activity_type': body.activity_type,
        'photo_path': body.photo_path,
        'number_limit_lower': body.number_limit_lower,
        'number_limit_upper': body.number_limit_upper,
        'price': body.price,
        'region_id': body.region_id,
        'region': body.region,
        'group_id': body.group_id,
        'group_name': body.group_name,
        'start_time': body.start_time,
        'end_time': body.end_time,
        'register_end_time': body.register_end_time,
        'activity_info': body.activity_info,
        'update_time': datetime.now(),
        'update_user': user_id,
    }
    pg_client.execute_commit(sql_update, params)
    return response_200(message='活动信息修改成功')


@app_activity.post("delete", summary='删除活动')
async def activity_delete(body: ActivityDeleteBody, user_id: str = Depends(token_client.token_verification)):
    # TODO 进行中和已结束的活动不能删除
    sql_delete = """
    UPDATE public.dim_activity
    SET activity_status = -1
    WHERE activity_id = %(activity_id)s AND activity_name = %(activity_name)s
    """
    params = {
        'activity_id': body.activity_id,
        'activity_name': body.activity_name
    }
    pg_client.execute_commit(sql_delete, params)

    return response_200(message=f'活动【{body.activity_name}】删除成功')
