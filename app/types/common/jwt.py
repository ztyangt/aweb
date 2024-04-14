from typing import Optional
from pydantic import BaseModel, Field


class JwtData(BaseModel):
    """jwt业务数据"""

    uid: int = Field(default=0)  # 用户id
    admin: Optional[bool] = Field(default=False)  # 是否管理员
    nickname: str = Field(default="")  # 用户姓名
