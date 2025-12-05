from langchain.agents import create_agent

from dotenv import load_dotenv
load_dotenv()

agent = create_agent(
    model="deepseek:deepseek-chat"
)

# print(agent)
# langgraph.graph.state.CompiledStateGraph
# Graph: nodes - edges 网状

# print (agent.nodes)
# {
#   '__start__': <langgraph.pregel._read.PregelNode object at 0x000001FD444BDC50>, 
#   'model': <langgraph.pregel._read.PregelNode object at 0x000001FD44A67250>
# }

## pregel: google 2010 发布的技术

results = agent.invoke({"messages":[{"role": "user", "content": "What is the weather in SF"}]})
# print (results)
# {'messages': [
#   HumanMessage(content='What is the weather in SF', additional_kwargs={}, response_metadata={}, id='d5f44d0b-1b34-41a8-b87f-ad014407b457'), 
#   AIMessage(content='I can\'t check real-time weather, but you can get the current weather in San Francisco from sources like:\n\n- Weather.com\n- AccuWeather\n- Your device\'s weather app\n- Searching "San Francisco weather" in your browser\n\nWould you like me to help you with something else related to weather planning?', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 64, 'prompt_tokens': 10, 'total_tokens': 74, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'prompt_cache_hit_tokens': 0, 'prompt_cache_miss_tokens': 10}, 'model_provider': 'deepseek', 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_ffc7281d48_prod0820_fp8_kvcache', 'id': '4fcb919a-40de-4a77-a294-05e669d4283d', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--cb39ff7c-750a-436a-9292-32b76d19eb3e-0', usage_metadata={'input_tokens': 10, 'output_tokens': 64, 'total_tokens': 74, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}})
# ]}

messages = results["messages"]
print (f"历史消息：{len(messages)} 条")
for message in messages:
    message.pretty_print()
