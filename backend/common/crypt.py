from passlib.context import CryptContext

from backend.common.singleton import SingletonMeta


class Crypt(metaclass=SingletonMeta):
    """
    加解密类
    """

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def encrypt(self, plain_text):
        """
        加密明文
        """
        return self.pwd_context.hash(plain_text)

    def verify_passwd(self, plain_passwd, hash_passwd):
        """
        校验密码
        """
        return self.pwd_context.verify(plain_passwd, hash_passwd)


crypt_client = Crypt()
