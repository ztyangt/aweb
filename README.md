# Aweb

基于 fastapi 的 web 开发模板

## 数据库迁移

1.  aerich init -t app.facade.database.config --location runtime/migrations
2.  aerich init-db
3.  aerich migrate
4.  aerich upgrade
