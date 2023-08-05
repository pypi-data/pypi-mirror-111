# Alembic

SqlAlachemy 数据库Migration管理工具


## 安装

[官方教程](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

1. pip install alembic 
	- 安装后在python环境会安装`alembic`命令行工具
2. alembic init `初始化目标目录` 
	- `初始化目标目录`可以不存在，但是不能是非空目录 
	- --template 可以指定模板（`alembic list_templates`查看模板）
3. alembic.ini alembic配置文件
4. alembic revision -m "" 创建迁移脚本
5. alembic upgrade head 迁移数据库变更
6. alembic history 查看数据库变更


## 自动迁移数据库

[官方教程](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)

- 修改`env.py`中`target_metadata`指向数据库模型的`metadata对象`
- 修改`alembic.ini`中要连接的数据库连接信息`sqlalachemy.url`
- 执行`alembic revision --autogenerate -m "init"`进行数据库合并脚本生成
- 执行`alembic upgrade head`升级到最新的修改
- 执行`alembic downgrade tag`降级到对应的版本
- 执行`alembic history`查看历史版本
