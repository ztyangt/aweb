from tortoise import fields
from app.model.base import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator


class ConfigModel(BaseModel):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=32, unique=True)
    value = fields.JSONField()

    create_time = fields.BigIntField(description="创建时间")
    update_time = fields.BigIntField(description="更新时间")

    class Meta:
        table = "config"


Config_Pydantic = pydantic_model_creator(ConfigModel, name="Config")
