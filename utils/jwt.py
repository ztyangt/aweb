import jwt
import toml
import pytz
from datetime import datetime, timedelta
from typing import Any
from pydantic import BaseModel


class JwtTokenBody(BaseModel):
    """ jwt数据格式"""
    sub: str  # 签发主题
    iss: str  # 签发者
    iat: datetime  # 签发时间
    exp: datetime  # 过期时间
    data: Any  # 业务数据


# token过期
TokenErrorTimeOut = "TokenTimeOut|token过期"
# token非法
TokenErrorInvalid = "TokenInvalid|token非法"


class JwtManageUtil(object):
    """
    JWT处理类
    """

    def __init__(self):
        config = toml.load('config/jwt.toml')
        self.algorithm = config.get('jwt').get(
            'algorithm', "HS256")
        self.subject = config.get('jwt').get(
            'subject', "Aweb")
        self.secretKey = config.get('jwt').get(
            'key', "Aweb-7dfa9589ccf3b93336fd22af3c77061e")
        self.expired = config.get('jwt').get('expire', 7200)
        self.iss = config.get('jwt').get('issuer', "ztyang")
        self.timezone = pytz.timezone(config.get(
            'jwt').get('timezone', "Asia/Shanghai"))

    def generate(self, payload: BaseModel) -> str:
        """
        生成 JWT
        :param payload: JwtTokenParam
        :return: str
        """
        # 当前时间 一定要设置时区，否则解析会报错： The token is not yet valid (iat)
        currentTime = datetime.now(self.timezone)
        jwtData = JwtTokenBody(
            sub=self.subject,
            iss=self.iss,
            iat=currentTime,
            exp=currentTime + timedelta(seconds=self.expired),
            data=payload
        )
        # 生成 JWT
        return jwt.encode(jwtData.model_dump(), self.secretKey, algorithm=self.algorithm)

    def decode(self, jwtToken: str, decodePydanticModel: Any) -> BaseModel | str:
        """
        解析 jwtToken
        :param jwtToken: str
        :param decodePydanticModel: BaseModel
        :return: BaseModel | bool
        """
        try:
            decoded_payload = jwt.decode(
                jwtToken, self.secretKey, algorithms=[self.algorithm])
            result = JwtTokenBody(**decoded_payload)
            return decodePydanticModel.parse_obj(result.data)
        except jwt.ExpiredSignatureError:
            return TokenErrorTimeOut
        except jwt.InvalidTokenError:
            return TokenErrorInvalid
        except Exception as e:
            return str(e)
