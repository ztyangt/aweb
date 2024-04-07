from pydantic import BaseModel, Field


class JwtData(BaseModel):
    """ jwt业务数据 """
    uid: int = Field(default=0)  # 用户id
    nickname: str = Field(default="")  # 用户姓名
