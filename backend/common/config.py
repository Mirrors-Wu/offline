class FileConfig:
    """
    文件相关配置
    """
    path = r'data'


class JwtConfig:
    """
    Jwt配置
    """
    secret_key = "b01c66dc2c58dc6a0aabfe2144256be36226de378bf87f72c0c795dda67f4d55"
    algorithm = "HS256"
    exp_minutes = 1440


class DataBaseConfig:
    """
    数据库配置
    """
    host = "120.26.168.84"
    port = 5432
    user = 'postgres'
    password = 'Mirrors0801!'
    database = 'offline'
