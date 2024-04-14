import re
from pydantic import BaseModel, Field, validator
from typing import List, Optional


class UserVal(BaseModel):
    # id: Optional[int] = Field(None,  example=1, description="用户id,存在更新,不存在则新增")
    account: str = Field(description="账号")
    nickname: str = Field(example="张三", description="用户名字")
    password: str = Field(description="用户密码")
    gender: int = Field(0, description="用户性别")
    avatar: str = Field(None, description="用户头像")
    email: str = Field(None, description="电子邮件")

    @validator("account")
    def account_validator(cls, v: str):
        if len(v) > 32:
            raise ValueError("账号长度不能超过32")
        if not v.encode().isalnum():
            raise ValueError("账号只能包含字母和数字")
        return v

    @validator("gender")
    def gender_validator(cls, v):
        if v not in [0, 1, 2]:
            raise ValueError("性别参数只能为0,1,2")
        return v

    @validator("password")
    def password_validator(cls, v):
        assert len(v) >= 6, "密码长度不能小于6"
        return v

    @validator("email")
    def email_validator(cls, v):
        pattern = r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
        if not re.match(pattern, v):
            raise ValueError("电子邮件格式不正确")
        return v


class UserUpdateVal(BaseModel):
    id: int = Field(None, example=1, description="用户id,存在更新,不存在则新增")
    account: str = Field(None, description="账号")
    nickname: str = Field(None, example="张三", description="用户昵称")
    password: str = Field(None, description="用户密码")
    gender: int = Field(None, description="用户性别")
    avatar: str = Field(None, description="用户头像")
    email: str = Field(None, description="电子邮件")

    @validator("account")
    def account_validator(cls, v: str):
        if len(v) > 32:
            raise ValueError("账号长度不能超过32")
        if not v.encode().isalnum():
            raise ValueError("账号只能包含字母和数字")
        return v

    @validator("gender")
    def gender_validator(cls, v):
        if v not in [0, 1, 2]:
            raise ValueError("性别参数只能为0,1,2")
        return v

    @validator("password")
    def password_validator(cls, v):
        assert len(v) >= 6, "密码长度不能小于6"
        return v

    @validator("email")
    def email_validator(cls, v):
        pattern = r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
        if not re.match(pattern, v):
            raise ValueError("电子邮件格式不正确")
        return v
