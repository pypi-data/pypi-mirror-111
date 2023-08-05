# SqlAlachemy 文档

> SqlAlachemy正在向`2.0`版本过渡，强烈建议使用`Style 2.0`语法，避免后面升级导致的不兼容性。

[Migration Doc](https://docs.sqlalchemy.org/en/14/changelog/migration_20.html)

SqlAlachemy 由`Core`和`ORM`组成。
- `Core`负责基础架构可以看作为数据库工具箱，主要负责管理数据库连接，数据库查询交互以及SQL的构造；
- `ORM`则负责提供可选的面向对象关系映射。


[1.4 学习教程](https://docs.sqlalchemy.org/en/14/tutorial/index.html)
[备注](https://docs.sqlalchemy.org/en/14/tutorial/index.html#a-note-on-the-future)

检查数据库版本
```python
import sqlalchemy
sqlalchemy.__version__
```
## 建立数据库连接
`engine`是数据库连接的中心引擎，管理数据库连接池，是数据库连接管理的全局实例。

```python
import sqlalchemy
engine = sqlalchemy.create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

# each 控制是否控制SQL日志显示
# future 参数控制是否启用`Style 2.0`语法
```

数据库连接URL由三部分组成：
1. 数据库方言名称，方言定义了特定数据库和DB-API结合的表现。
2. 数据库驱动名称
3. 数据库连接信息

当数据库引擎初始化时，并未产生于数据库实际的连接，只有当进行`connect()`操作或者查询发生时，才会进行真正的数据库连接。
[Dialect](https://docs.sqlalchemy.org/en/14/core/internals.html#sqlalchemy.engine.Dialect)
[create_engine 初始化参数](https://docs.sqlalchemy.org/en/14/core/engines.html#sqlalchemy.create_engine)
[数据库连接配置](https://docs.sqlalchemy.org/en/14/core/engines.html)


## 与数据库事务和API的交互
session对象时`Connection/Result`对象的facade编程模式的facade

使用`text()`构造原生查询

```python
# commit as you go
# 同一上下文中可以进行多次提交，且如果存在未提交事务，在退出上下文时会进行事务回滚
with engine.connection() as conn:
	# 事务块1
	conn.commit()

	# 事务块2
	conn.commit()


# begin once
# 此事务块会在上下文退出时自动进行事务提交
with engine.begin() as conn:
	# 事务块
	...

```

ORM的数据库事务和连接管理对象是`Session`，当与非ORM结构一起使用时，它会传递SQL语句和connection区别不大。
session并没有始终保持相同的连接，而是在每次事务结束后创建新的连接

## 数据库元数据

数据库概念的表示对象成为数据库元数据。
数据库元数据中常见的基本对象是`MetaData`,`Table`,`Column`
MetaData也可看作是存储table信息的对象。

数据库里表可以用对象的集合进行表示，该集合存储表的一系列对象，我们称该集合表示对象为`MetaData`对象。

### 数据库表的声明方式

- 通过Table(metadata, Column()...)声明，需要全局声明metadata对象进行声明
- 通过继承`declarative_base()`创建的数据库表基类通过继承来进行声明



## 数据库数据


利用核心功能`insert()/select()/update()/delete()`通过生成特定语言SQL语句结合数据库连接connection来操作数据库。
利用ORM对象操作数据库。

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)


可以通过在类中指定`__table__`属性，此属性对应Table声明对象进行声明。


