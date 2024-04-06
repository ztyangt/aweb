from tortoise import fields
from app.model.base import BaseModel


class UserModel(BaseModel):
    account = fields.CharField(max_length=32, description="账号")
    nickname = fields.CharField(max_length=32, description="用户名")
    avatar = fields.CharField(max_length=128, description="头像")
    email = fields.CharField(max_length=32, description="邮箱")
    gender = fields.IntField(0, description="性别")
    password = fields.CharField(max_length=32, description="密码")

    class Meta:
        table_name = "fw_user"
        field_name = "f_{}"
