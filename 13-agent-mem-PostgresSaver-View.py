# PostgreSQL checkpoint 查看程序
from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = "postgresql://postgres:123456@localhost:5432/postgres?sslmode=disable"

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    # 获取所有checkpoint
    checkpoints = checkpointer.list(
        {"configurable": {"thread_id": "1"}}
    )
    
    for checkpoint in checkpoints:
        messages = checkpoint[1]["channel_values"]["messages"]
        for message in messages:
            message.pretty_print()
        break
