import re
from pydantic import BaseModel, Field, validator
from typing import List, Optional


class ConfigVal(BaseModel):
    name: str = Field(description="配置名")
    value: dict = Field({}, description="配置值")
