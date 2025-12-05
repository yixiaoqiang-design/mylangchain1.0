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

print (agent.nodes)
# {
#   '__start__': <langgraph.pregel._read.PregelNode object at 0x000002DE262EC490>, 
#   'model': <langgraph.pregel._read.PregelNode object at 0x000002DE262EC710>, 
#   'tools': <langgraph.pregel._read.PregelNode object at 0x000002DE2631A890>
# }

results = agent.invoke({"messages":[
    {"role": "user", "content": "What is the weather in SF"}]})
    # {"role": "user", "content": "How many people in SF"}]})

messages = results["messages"]
print (f"历史消息：{len(messages)} 条")
for message in messages:
    message.pretty_print()
