# Microservice Name

## 初始化环境

### 安装python包

```shell
pip install dapr dapr-ext-fastapi
```

### 项目结构
- alembic `alembic`记录历史
- config 配置文件目录
  - dev.yaml 开发配置
  - prod.yaml 生产配置
- doc 文档目录，包括：http请求文档
- service 服务代码目录
  - main.py 服务app模块文件
  - deps.py 共享依赖模块文件
  - models.py 模型模块文件，可以将其升级为models目录，拆分代码为多个文件
  - routers.py 路由模块文件，可以将其升级为routers目录，拆分代码为多个文件
  - schemas.py 校检模块文件，同上
  - middlewares.py 中间件模块，同上
- tests 服务测试代码目录
- .gitignore git忽略文件设置文件
- Dockerfile dockerfile文件
- Makefile make运行命令
- README.md 说明文档
- requirements.txt python依赖包生成文件

### ORM使用

- 使用`SqlAlachemy`进行数据库的操作，为了考虑后向兼容问题，建议使用版本`1.4+`，另建议使用`Style 2.0`编码样式进行编码。
- 使用`alembic`进行数据库表变动管理，方便对数据库结构变动进行追踪和维护。


[Style 2.0](https://docs.sqlalchemy.org/en/14/tutorial/index.html)
[Alembic](./doc/alembic.md)

## 设计要点


## 实现思路


## 接口设计


## 备注


## 参考

[FastAPI Project Structure Reference](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
