## 安装 PostgreSQL 
# https://www.postgresql.org/download/windows/
# 1）user:postgres/xxxxxx
# 2）port:5432
# 3）把 D:\PostgreSQL\18\bin 配置到环境变量path里面

## 工具
# psql -U postgres -h localhost -p 5432

## 主要命令：
#   \l 列出所有数据库
#   \dt 列出所有数据表
#   \d <table>  查看表结构
#   删除表：DROP TABLE checkpoint_blobs, checkpoint_migrations, checkpoint_writes, checkpoints CASCADE;
#   SELECT * from <table> 查看数据
#   \q 退出

## pip install psycopg langgraph-checkpoint-postgres

## DB_URI="postgresql://postgres:123456@localhost:5432/postgres?sslmode=disable"

from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver

from dotenv import load_dotenv
load_dotenv()

DB_URI="postgresql://postgres:123456@localhost:5432/postgres?sslmode=disable"

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()  # 创建数据表，只运行一次

    agent = create_agent(
        model="deepseek:deepseek-chat",
        checkpointer=checkpointer
    )

    config = {"configurable":{"thread_id":"1"}}

    # 第一轮问答
    # 问
    results = agent.invoke(
        {"messages":[{"role": "user", "content": "来一首宋词"}]},
        config=config
    )

    # 答
    messages = results["messages"]
    print (f"历史消息：{len(messages)} 条")
    for message in messages:
        message.pretty_print()

    # 第二轮问答
    # 问
    results = agent.invoke(
        {"messages":[{"role": "user", "content": "再来"}]},
        config=config
    )

    # 答
    messages = results["messages"]
    print (f"历史消息：{len(messages)} 条")
    for message in messages:
        message.pretty_print()
