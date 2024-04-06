from tortoise import Model, fields


class BaseModel(Model):
    id = fields.IntField(pk=True)
    # 自动在创建记录时设置的时间戳
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    # 自动在每次更新记录时设置的时间戳
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    # JSON字段，可以存储任意结构的数据
    json = fields.JSONField(default={}, description="JSON数据")
    # 文本备注字段
    remark = fields.CharField(max_length=255, null=True, description="备注")
    # 通用文本字段
    text = fields.CharField(max_length=1024, null=True, description="文本内容")

    class Meta:
        abstract = True  # 抽象模型，不会在数据库中创建表
