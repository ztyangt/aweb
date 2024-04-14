from tortoise import Model
from typing import Coroutine, Iterable, Any
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise import timezone


class BaseModel(Model):

    def _pre_save(self, using_db: BaseDBAsyncClient | None = None, update_fields: Iterable[str] | None = None) -> Coroutine[Any, Any, None]:
        print("保存数据")
        if hasattr(self, "create_time") and self.create_time is None:
            self.create_time = int(timezone.now().timestamp() * 1000)

        if hasattr(self, "update_time") and self.update_time is None:
            self.update_time = self.create_time if hasattr(
                self, "create_time") else int(timezone.now().timestamp() * 1000)
        return super()._pre_save(using_db, update_fields)

    def _post_save(self, using_db: BaseDBAsyncClient | None = None, created: bool = False, update_fields: Iterable[str] | None = None) -> Coroutine[Any, Any, None]:
        return super()._post_save(using_db, created, update_fields)

    def _pre_delete(self, using_db: BaseDBAsyncClient | None = None) -> Coroutine[Any, Any, None]:
        return super()._pre_delete(using_db)

    def _post_delete(self, using_db: BaseDBAsyncClient | None = None) -> Coroutine[Any, Any, None]:
        return super()._post_delete(using_db)

    class Meta:
        abstract = True
