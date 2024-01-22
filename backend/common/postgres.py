import psycopg2

from backend.common.config import DataBaseConfig
from backend.common.singleton import SingletonMeta


class PostgresClient(metaclass=SingletonMeta):
    """
    数据库工具类
    //TODO 使用连接池
    // TODO 连接异常断开，待排查
    """

    def __init__(self):
        self.conn = None
        self.cur = None
        self.connect()

    def connect(self):
        self.conn = psycopg2.connect(host=DataBaseConfig.host,
                                     port=DataBaseConfig.port,
                                     database=DataBaseConfig.database,
                                     user=DataBaseConfig.user,
                                     password=DataBaseConfig.password
                                     )
        self.cur = self.conn.cursor()

    def check_connect(self):
        if self.conn.closed:
            self.connect()

    def execute_commit(self, query, params=None):
        self.check_connect()

        self.cur.execute(query, params)
        self.conn.commit()

    def execute_select(self, query, params=None):
        self.check_connect()

        self.cur.execute(query, params)
        rows = self.cur.fetchall()
        return rows

    def execute_file(self, path):
        """
        执行sql文件
        """
        with open(path, 'r', encoding='utf-8') as sql_file:
            sql_content = sql_file.read()
            self.execute_commit(sql_content)


pg_client = PostgresClient()
