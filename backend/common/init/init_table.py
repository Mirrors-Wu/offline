# 初始化数据库
from backend.common.postgres import pg_client


def init_table():
    pg_client.execute_file('common/init/init_table.sql')
