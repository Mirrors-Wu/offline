from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from backend.common.responses import response_200

from backend.common.postgres import pg_client
from backend.common.token import token_client
from backend.schemas.dict_schema import *

app_dict = APIRouter()


@app_dict.post("/dict_type/create", summary='新建字典类型')
async def app_dict_dict_type_create(body: DictTypeCreateBody, user_id: str = Depends(token_client.token_verification)):
    # 判断字典类型是否已存在
    sql_cate = """
        SELECT dict_type
        FROM public.dim_dict_type
        WHERE dict_type = %(dict_type)s
        """
    rows = pg_client.execute_select(sql_cate, {'dict_type': body.dict_type})

    if rows:
        raise HTTPException(status_code=400, detail=f'字典类型【{body.dict_type}】已存在')

    sql_create = """
        INSERT INTO public.dim_dict_type (dict_type, status, notes, create_time, create_user, update_time, update_user)
        VALUES (%(dict_type)s, %(status)s, %(notes)s, %(create_time)s, %(create_user)s, %(update_time)s, %(update_user)s) 
        """
    params = {
        'dict_type': body.dict_type,
        'status': '1',
        'notes': body.notes,
        'create_time': datetime.now(),
        'create_user': user_id,
        'update_time': datetime.now(),
        'update_user': user_id
    }
    pg_client.execute_commit(sql_create, params)

    return response_200(message='新建成功')


@app_dict.post("/dict_type/get", response_model=DictTypeGetResp, summary='查询字典类型')
async def app_dict_dict_type_get(user_id: str = Depends(token_client.token_verification)):
    sql_cate = """
        SELECT dict_type_id,
               dict_type,
               status, 
               notes, 
               TO_CHAR(create_time, 'YYYY-MM-DD HH24:MI:SS'), 
               create_user, 
               TO_CHAR(update_time, 'YYYY-MM-DD HH24:MI:SS'), 
               update_user
        FROM public.dim_dict_type
        """
    rows = pg_client.execute_select(sql_cate)

    return response_200(data={'dict_type_list': [{'dict_type_id': i[0],
                                                  'dict_type': i[1],
                                                  'status': i[2],
                                                  'notes': i[3],
                                                  'create_time': i[4],
                                                  'create_user': i[5],
                                                  'update_time': i[6],
                                                  'update_user': i[7],
                                                  } for i in rows]
                              }
                        )


@app_dict.post("/dict_type/edit", summary='编辑字典类型')
async def app_dict_dict_type_edit(body: DictTypeEditBody, user_id: str = Depends(token_client.token_verification)):
    sql = ''
    if body.dict_type:
        sql += """
        UPDATE public.dim_dict_type 
        SET dict_type = %(dict_type)s, update_time = %(update_time)s, update_user = %(update_user)s
        WHERE dict_type_id = %(dict_type_id)s;
        """
    if body.notes:
        sql += """
        UPDATE public.dim_dict_type 
        SET notes = %(notes)s, update_time = %(update_time)s, update_user = %(update_user)s
        WHERE dict_type_id = %(dict_type_id)s;
        """
    if body.status:
        sql += """
        UPDATE public.dim_dict_type 
        SET status = %(status)s, update_time = %(update_time)s, update_user = %(update_user)s
        WHERE dict_type_id = %(dict_type_id)s;
        """
    params = {
        'dict_type_id': body.dict_type_id,
        'dict_type': body.dict_type,
        'status': body.status,
        'notes': body.notes,
        'update_time': datetime.now(),
        'update_user': user_id,
    }
    pg_client.execute_commit(sql, params)

    return response_200(message='编辑成功')


@app_dict.post("/dict_type/delete", summary='删除字典类型')
async def app_dict_dict_type_delete(body: DictTypeDeleteBody, user_id: str = Depends(token_client.token_verification)):
    # TODO 删除时需要同步删除对应的字典标签
    sql_create = """
        DELETE FROM public.dim_dict_type 
        WHERE dict_type_id = %(dict_type_id)s
        AND dict_type = %(dict_type)s
        """
    params = {'dict_type_id': body.dict_type_id, 'dict_type': body.dict_type}
    pg_client.execute_commit(sql_create, params)

    return response_200(message='删除成功')


@app_dict.post("/dict_data/create", summary='新建字典标签')
async def app_dict_dict_data_create(body: DictDataCreateBody, user_id: str = Depends(token_client.token_verification)):
    # 字典标签值是否已存在
    sql_value = """
        SELECT dict_name
        FROM public.dim_dict_data
        WHERE dict_name = %(dict_name)s
        AND dict_type = %(dict_type)s
    """
    if pg_client.execute_select(sql_value, {'dict_name': body.dict_name,
                                            'dict_type': body.dict_type}):
        raise HTTPException(status_code=400, detail=f'字典标签已存在')

    # 新建
    sql_create = """
        INSERT INTO public.dim_dict_data 
        (dict_name, dict_type_id, dict_type, dict_value, create_time, create_user, update_time, update_user)
        VALUES (%(dict_name)s, %(dict_type_id)s, %(dict_type)s, %(dict_value)s, %(create_time)s, %(create_user)s, %(update_time)s, %(update_user)s) 
        """
    params = {
        'dict_name': body.dict_name,
        'dict_type_id': body.dict_type_id,
        'dict_type': body.dict_type,
        'dict_value': body.dict_value,
        'create_time': datetime.now(),
        'create_user': user_id,
        'update_time': datetime.now(),
        'update_user': user_id
    }
    pg_client.execute_commit(sql_create, params)

    return response_200(message='创建成功')


@app_dict.post("/dict_data/get", response_model=DictDataGetResp, summary='查询字典标签')
async def app_dict_dict_data_get(body: DictDataGetBody, user_id: str = Depends(token_client.token_verification)):
    sql_get = """
        SELECT 
        dict_id, 
        dict_name, 
        dict_type_id, 
        dict_type, 
        dict_value, 
        TO_CHAR(create_time, 'YYYY-MM-DD HH24:MI:SS'), 
        create_user, 
        TO_CHAR(update_time, 'YYYY-MM-DD HH24:MI:SS'), 
        update_user
        FROM public.dim_dict_data
        WHERE dict_type_id = %(dict_type_id)s
        AND dict_type = %(dict_type)s
        """
    rows = pg_client.execute_select(sql_get, {'dict_type_id': body.dict_type_id, 'dict_type': body.dict_type})

    return response_200(data={'dict_list': [{'dict_id': i[0],
                                             'dict_name': i[1],
                                             'dict_type_id': i[2],
                                             'dict_type': i[3],
                                             'dict_value': i[4],
                                             'create_time': i[5],
                                             'create_user': i[6],
                                             'update_time': i[7],
                                             'update_user': i[8],
                                             } for i in rows]
                              })


@app_dict.post("/dict_data/edit", summary='编辑字典标签')
async def app_dict_dict_data_edit(body: DictDataEditBody, user_id: str = Depends(token_client.token_verification)):
    sql = ''
    if body.dict_name:
        sql += """
        UPDATE public.dim_dict_data 
        SET dict_name = %(dict_name)s, update_time = %(update_time)s, update_user = %(update_user)s
        WHERE dict_id = %(dict_id)s;
        """
    if body.dict_type_id:
        sql += """
        UPDATE public.dim_dict_data 
        SET dict_type_id = %(dict_type_id)s, dict_type = %(dict_type)s, update_time = %(update_time)s, update_user = %(update_user)s
        WHERE dict_id = %(dict_id)s;
        """
    if body.dict_value:
        sql += """
                UPDATE public.dim_dict_data 
                SET dict_value = %(dict_value)s, update_time = %(update_time)s, update_user = %(update_user)s
                WHERE dict_id = %(dict_id)s;
                """
    params = {
        'dict_id': body.dict_id,
        'dict_name': body.dict_name,
        'dict_type_id': body.dict_type_id,
        'dict_type': body.dict_type,
        'update_time': datetime.now(),
        'update_user': user_id
    }
    pg_client.execute_commit(sql, params)

    return response_200(message='修改成功')


@app_dict.post("/dict_data/delete", summary='删除字典标签')
async def app_dict_dict_data_delete(body: DictDataDeleteBody, user_id: str = Depends(token_client.token_verification)):
    sql_update = """ 
        DELETE FROM public.dim_dict_data 
        WHERE dict_id = %(dict_id)s and dict_name = %(dict_name)s
        """
    params = {
        'dict_id': body.dict_id,
        'dict_name': body.dict_name
    }
    pg_client.execute_commit(sql_update, params)

    return response_200(message='删除成功')
