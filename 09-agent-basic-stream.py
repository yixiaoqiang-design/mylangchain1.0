from langchain.agents import create_agent

from dotenv import load_dotenv
load_dotenv()

def get_weather(city: str) -> str:
    """Get weather for a given city"""
    return f"It's alwasy sunny in {city}!"

agent = create_agent(
    model="deepseek:deepseek-chat",
    tools=[get_weather]
)

### 流式输出方式1： message by message 
# for event in agent.stream(
#     {"messages":[{"role": "user", "content": "What is the weather in SF"}]},
#     stream_mode="values"  # message by message 
# ):
#     messages = event["messages"]
#     print (f"历史消息：{len(messages)} 条")
#     # for message in messages:
#     #     message.pretty_print()
#     messages[-1].pretty_print()

### 流式输出方式2： token by token 
for chunk in agent.stream(
    {"messages":[{"role": "user", "content": "What is the weather in SF"}]},
    stream_mode="messages"  # token by token
):
    print (chunk[0].content, end='')
    # print (chunk)
    # (
    # AIMessageChunk(
    #   content=' San', 
    #   additional_kwargs={}, 
    #   response_metadata={'model_provider': 'deepseek'}, 
    #   id='lc_run--c70141f6-db06-4f3c-b6c7-9c80e4c077aa'
    # ), 
    # {
    #   'langgraph_step': 3, 
    #   'langgraph_node': 'model', 
    #   'langgraph_triggers': ('branch:to:model',), 
    #   'langgraph_path': ('__pregel_pull', 'model'), 
    #   'langgraph_checkpoint_ns': 'model:94df551b-96b2-2c7d-d65c-c9b71904b205', 
    #   'checkpoint_ns': 'model:94df551b-96b2-2c7d-d65c-c9b71904b205', 
    #   'ls_provider': 'deepseek', 
    #   'ls_model_name': 'deepseek-chat', 
    #   'ls_model_type': 'chat', 
    #   'ls_temperature': None
    # }
    # )