from datetime import datetime, timedelta

import jwt
from fastapi import Header, HTTPException, Response

from backend.common.config import JwtConfig
from backend.common.singleton import SingletonMeta


class Token(metaclass=SingletonMeta):
    def __init__(self):
        self.private_key = JwtConfig.secret_key

    def token_generation(self, user_id, expire_minutes=1440):
        """
        生成token
        """
        # 设置过期时间
        expires_at = datetime.utcnow() + timedelta(minutes=expire_minutes)

        # 构建payload
        payload = {'exp': expires_at,
                   'user_id': user_id}

        # 生成 token
        token = jwt.encode(payload, self.private_key, algorithm='HS256')
        return token

    def token_verification(self, response: Response, token: str = Header(...)):
        try:
            # 解码 token
            decoded_token = jwt.decode(token, self.private_key, algorithms=['HS256'])
            return decoded_token['user_id']
        except jwt.ExpiredSignatureError:
            # token已过期
            raise HTTPException(status_code=401, detail='token已过期')
        except jwt.InvalidTokenError:
            # token不合法
            raise HTTPException(status_code=401, detail='token无效')


token_client = Token()
