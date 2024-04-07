from tortoise import fields
from app.model.base import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator


class UserModel(BaseModel):
    id = fields.IntField(pk=True)
    account = fields.CharField(max_length=32, description="账号", unique=True)
    nickname = fields.CharField(max_length=32, description="用户名")
    avatar = fields.CharField(max_length=128, description="头像", null=True)
    email = fields.CharField(
        max_length=32, description="邮箱", unique=True, null=True)
    gender = fields.IntField(default=0, description="性别")
    password = fields.CharField(max_length=60, description="密码")

    # 公共字段
    expand = fields.JSONField(null=True, description="扩展数据")
    remark = fields.CharField(max_length=255, null=True, description="备注")
    text = fields.CharField(max_length=1024, null=True, description="文本内容")
    create_time = fields.BigIntField(description="创建时间")
    update_time = fields.BigIntField(description="更新时间")
    delete_time = fields.BigIntField(null=True, description="删除时间")

    class Meta:
        table = "users"

    def result(self) -> dict:
        return {}

    class PydanticMeta:
        computed = ["result"]
        exclude = ["password"]


User_Pydantic = pydantic_model_creator(UserModel, name="User")
