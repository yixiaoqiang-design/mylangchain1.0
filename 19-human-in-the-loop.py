## 人在回路，human-in-the-loop
## agent， 集成大模型，集成工具，工具调用时候，提供中断机制，
## 人的确认： approve, reject, edit 
## 中间件， middleware

### 更复杂一点的智能体 create_agent
## 大模型：model
## 系统提示词：system_prompt - new
## 工具：tools, 用户消息传递参数
#   =>工具运行时上下文传递参数：context_schema - new
## 记忆管理：checkpointer
## 结构化输出：response_format - new

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool, ToolRuntime

from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.types import Command

from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()

# 系统提示词
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location.

用中文回答
"""

# 用户消息传递参数
@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

# 工具运行时上下文传递参数
@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"

# 结构化输出
@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    # A punny response (always required)
    punny_response: str
    # Any interesting information about the weather if available
    weather_conditions: str | None = None

# 记忆管理
checkpointer = InMemorySaver()

# 创建智能体
agent = create_agent(
    model="deepseek:deepseek-chat",
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "get_user_location": True, # 所有决策都允许， approve, reject, edit 
                "get_weather_for_location": {
                    "allowed_decisions": ["approve", "reject"]
                }
            }, 
            description_prefix="工具执行挂起等待决策："
        )
    ],
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer
)

# 配置 thead_id
config = {"configurable": {"thread_id": "1"}}

# 问问题
response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather outside?"}]},
    config=config,
    context=Context(user_id="1")
)

# print(response['structured_response'])

messages = response["messages"]
print(f"历史消息：{len(messages)}")
for message in messages:
    message.pretty_print()

if "__interrupt__" in response: # dict, 判断response 是否有key：__interupt__
    print("INTERRUPED")
    interrupt = response["__interrupt__"][0]
    for request in interrupt.value["action_requests"]:
        print (request["description"])


# 指令
response = agent.invoke(
    Command(
        resume={"decisions": [
            {"type": "approve"}
        ]},
    ),
    config=config,
    context=Context(user_id="1")
)

messages = response["messages"]
print(f"历史消息：{len(messages)}")
for message in messages:
    message.pretty_print()

if "__interrupt__" in response: # dict, 判断response 是否有key：__interupt__
    print("INTERRUPED")
    interrupt = response["__interrupt__"][0]
    for request in interrupt.value["action_requests"]:
        print (request["description"])


# 第  2 个 指令
response = agent.invoke(
    Command(
        resume={"decisions": [
            {"type": "approve"}
        ]},
    ),
    config=config,
    context=Context(user_id="1")
)

messages = response["messages"]
print(f"历史消息：{len(messages)}")
for message in messages:
    message.pretty_print()

if "__interrupt__" in response: # dict, 判断response 是否有key：__interupt__
    print("INTERRUPED")
    interrupt = response["__interrupt__"][0]
    for request in interrupt.value["action_requests"]:
        print (request["description"])