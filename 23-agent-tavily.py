### 本示例展示 agent 如何使用搜索引擎 tavily
### tavily: 搜索引擎：给 agent 用的，提供两种api：
# tavily_search
# tavily_extract
# https://www.tavily.com/ 
# 注册，自动获取获取 TAVILY_API_KEY="..." 
# 放到 .env 里面, 
# 1000次/月，免费的

## pip install tavily-python langchain-tavily

from langchain.agents import create_agent

from dotenv import load_dotenv
load_dotenv()

from tavily import TavilyClient
from typing import Literal

tavilyClient = TavilyClient()

def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavilyClient.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )

# System prompt to steer the agent to be an expert researcher
research_instructions = """
你是一个专业的研究员。你的任务是进行彻底的研究并撰写一份完整的报告。
    
你可以使用以下工具：
- internet_search: 用于搜索互联网信息
    
请确保：
1. 进行全面的搜索来收集信息
2. 验证信息的准确性
3. 组织信息并撰写结构化的报告
"""

agent = create_agent(
    model="deepseek:deepseek-chat",
    tools=[internet_search],
    system_prompt=research_instructions
)

for event in agent.stream(
    {"messages":[{"role": "user", 
    "content": "什么是langgraph？详细介绍它的功能、用途和主要特点。"}]
    },
    stream_mode="values"
):
    event["messages"][-1].pretty_print()
