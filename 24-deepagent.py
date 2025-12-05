## deepagent: planning, file system, subagent
## demo: research agent: research, report

## pip install deepagents 

### 过程：
#  deepagent 内置工具：write_todos, to do list
#  用户定义的工具：internet_search .... update to do list 
#  deepagent 内置工具：write_file, 写报告


# from langchain.agents import create_agent
from deepagents import create_deep_agent

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
4. 务必最后调用 write_file 输出报告
"""

agent = create_deep_agent(
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
    if "files" in event:
        print ("*"*80)
        print (event["files"])
    event["messages"][-1].pretty_print()
