from langchain.agents import create_agent

from dotenv import load_dotenv
load_dotenv()

agent = create_agent(
    model="deepseek:deepseek-chat"
)

# 第一轮问答
# 问
results = agent.invoke({
    "messages":[{"role": "user", "content": "来一首宋词"}]})

# 答
messages = results["messages"]
print (f"历史消息：{len(messages)} 条")
for message in messages:
    message.pretty_print()

his_messages = messages

# 第二轮问答
# 问
message = {"role": "user", "content": "再来"}
his_messages.append(message)
results = agent.invoke({
    "messages":his_messages})

# 答
messages = results["messages"]
print (f"历史消息：{len(messages)} 条")
for message in messages:
    message.pretty_print()
