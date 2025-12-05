from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

model=init_chat_model(
    model="deepseek:deepseek-chat", 
    temperature=0.1
)

import requests, pathlib

url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
local_path = pathlib.Path("Chinook.db")

if local_path.exists():
    print(f"{local_path} already exists, skipping download.")
else:
    response = requests.get(url)
    if response.status_code == 200:
        local_path.write_bytes(response.content)
        print(f"File downloaded and saved as {local_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")


from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///Chinook.db")

print(f"数据库: {db.dialect}")
print(f"数据表: {db.get_usable_table_names()}")
print(f'艺术家(Artist)示例: {db.run("SELECT * FROM Artist LIMIT 5;")}')


from langchain_community.agent_toolkits import SQLDatabaseToolkit

toolkit = SQLDatabaseToolkit(db=db, llm=model)

tools = toolkit.get_tools()
for tool in tools:
    print(f"可用工具：{tool.name}: {tool.description}\n")


system_prompt = """
您是一个用于与SQL数据库交互的智能体。
给定一个输入问题，首先创建一个语法正确的{dialect}查询语句，
然后查看查询结果并返回答案。除非用户明确指定他们希望获取的具体示例数量，
否则始终将查询结果限制在最多{top_k}条。

您可以通过相关列对结果进行排序，以返回数据库中最有意义的示例。
永远不要查询特定表的所有列，只询问与问题相关的列。

在执行查询之前，您必须仔细检查查询语句。如果在执行查询时出现错误，
请重新编写查询并重试。

不要对数据库执行任何DML语句（INSERT、UPDATE、DELETE、DROP等）。

开始时，您应该始终先查看数据库中的表，以了解可以查询什么。不要跳过此步骤。

然后您应该查询最相关表的模式结构。
""".format(
    dialect=db.dialect,
    top_k=5,
)

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware 
from langgraph.checkpoint.memory import InMemorySaver 

agent = create_agent(
    model,
    tools,
    system_prompt=system_prompt,
    middleware=[ 
        HumanInTheLoopMiddleware( 
            interrupt_on={"sql_db_query": True}, 
            description_prefix="Tool execution pending approval", 
        ), 
    ], 
    checkpointer=InMemorySaver(), 
)

question = "哪个流派的曲目平均长度最长？"
config = {"configurable": {"thread_id": "1"}} 

decisions = [{"type": "reject"}]

for step in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    config, 
    stream_mode="values",
):
    if "messages" in step:
        step["messages"][-1].pretty_print()
    if "__interrupt__" in step: 
        print("INTERRUPTED:") 
        interrupt = step["__interrupt__"][0] 
        for request in interrupt.value["action_requests"]: 
            print(request["description"])
        # 获取用户输入
        user_input = input("\n请输入您的决定 (approve/reject/edit): ").strip().lower()
        if user_input == "approve":
            decisions = [{"type": "approve"}]
        elif user_input == "reject":
            decisions = [{"type": "reject"}] 
        elif user_input == "edit":
            decisions = [{"type": "edit"}]
        else:
            print("无效输入，默认批准")
            decisions = [{"type": "approve"}]
         
    else:
        pass

from langgraph.types import Command 

for step in agent.stream(
    Command(resume={"decisions": decisions}),
    config,
    stream_mode="values",
):
    if "messages" in step:
        step["messages"][-1].pretty_print()
    if "__interrupt__" in step:
        print("INTERRUPTED:")
        interrupt = step["__interrupt__"][0]
        for request in interrupt.value["action_requests"]:
            print(request["description"])
    else:
        pass