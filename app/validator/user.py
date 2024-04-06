import re
from pydantic import BaseModel, Field, validator
from typing import List, Optional


class UserVal(BaseModel):
    id: Optional[int] = Field(None,  example=1, description="用户id,存在更新,不存在则新增")
    name: str = Field(example="张三", description="用户名字")
    age: Optional[int] = Field(None,  example=99, description="用户年龄")
    password: str = Field(description="用户密码")
    email: Optional[str] = Field(None, description="电子邮件")

    @validator("password")
    def password_validator(cls, v):
        assert len(v) >= 6, "密码长度不能小于6"
        return v

    @validator("email")
    def email_validator(cls, v):
        if v is None:
            return v
        pattern = r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
        if not re.match(pattern, v):
            raise ValueError("电子邮件地址格式不正确")
        return v
