import toml
import pytz
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Any
from pydantic import BaseModel
from passlib.context import CryptContext
from app.model.base.user import UserModel
from fastapi import Request, HTTPException, status


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JwtTokenBody(BaseModel):
    """jwt数据格式"""

    sub: str  # 签发主题
    iss: str  # 签发者
    iat: datetime  # 签发时间
    exp: datetime  # 过期时间
    data: Any  # 业务数据


JWTConfig = toml.load("config/jwt.toml")
algorithm = JWTConfig.get("jwt").get("algorithm", "HS256")
subject = JWTConfig.get("jwt").get("subject", "Aweb")
secretKey = JWTConfig.get("jwt").get("key", "Aweb-7dfa9589ccf3b93336fd22af3c77061e")
expired = JWTConfig.get("jwt").get("expire", 7200)
iss = JWTConfig.get("jwt").get("issuer", "ztyang")
timezone = pytz.timezone(JWTConfig.get("jwt").get("timezone", "Asia/Shanghai"))


class JwtUtil:
    """
    JWT处理类
    """

    @staticmethod
    def generate(payload: dict) -> str:
        # 当前时间 一定要设置时区，否则解析会报错： The token is not yet valid (iat)
        currentTime = datetime.now(timezone)
        jwtData = JwtTokenBody(
            sub=subject,
            iss=iss,
            iat=currentTime,
            exp=currentTime + timedelta(seconds=expired),
            data=payload,
        )
        # 生成 JWT
        return jwt.encode(jwtData.model_dump(), secretKey, algorithm=algorithm)

    @staticmethod
    def check_admin(request: Request):
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="请先登录！"
            )
        try:
            payload = jwt.decode(token, secretKey, algorithms=[algorithm])
            if not payload["data"].get("admin", False):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="无操作权限！",
                    headers=dict(WWW_Authenticate="Bearer"),
                )
            return payload["data"]
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="登录已过期，请重新登录！",
            )

    @staticmethod
    def check_login(request: Request):
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="请先登录！"
            )
        try:
            payload = jwt.decode(token, secretKey, algorithms=[algorithm])
            return payload["data"]
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="登录已过期，请重新登录！",
            )

    @staticmethod
    async def get_current_user(request: Request):
        pass


class handleAuth:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    async def authenticate_user(account: str, password: str):
        user = await UserModel.get_or_none(account=account)
        if not user:
            return False
        if not handleAuth.verify_password(password, user.password):
            return False
        return user
