from pydantic import BaseModel, Field, validator
from typing import List, Optional


class TestVal(BaseModel):
    ids: List[int]
    name: str = Field(example="张三", description="用户名字")
    age: Optional[int] = Field(None,  example=99, description="用户年龄")
    password: str = Field(description="用户密码")

    @validator("password")
    def password_validator(cls, v):
        assert len(v) >= 6, "密码长度不能小于6"
        return v
