## checkpointer: 检查点管理器， 存储
## checkpoint：检查点，状态图的总体状态快照
## thread_id 管理
## 作用：记忆管理、时间旅行(time travel)、pause(human-in-the-loop)、容错

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver # checkpointer

from langchain_core.runnables import RunnableConfig
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

# 表达状态: 是整个状态图的状态
class State(TypedDict):
    foo: str
    bar: Annotated[list[str], add]

def node_a(state: State):
    return {"foo": "a", "bar": ["a"]}

def node_b(state: State):
    return {"foo": "b", "bar": ["b"]}

# 构建状态图
workflow = StateGraph(State)
workflow.add_node(node_a)
workflow.add_node(node_b)
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

# 检查点管理器：
checkpointer = InMemorySaver()

# 编译
graph = workflow.compile(checkpointer=checkpointer)

# 配置
config: RunnableConfig = {
    "configurable":{"thread_id": "1"}
}
# 调用
results = graph.invoke({"foo":""}, config)
print (results)
# {'foo': 'b', 'bar': ['a', 'b']}

## 状态查看
# print(graph.get_state(config))
# StateSnapshot(
#   values={'foo': 'b', 'bar': ['a', 'b']}, 
#   next=(), 
#   config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f0bab9c-0143-66a5-8002-b2b07f7020b5'}}, 
#   metadata={'source': 'loop', 'step': 2, 'parents': {}}, 
#   created_at='2025-11-06T02:39:00.275165+00:00', 
#   parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f0bab9c-013f-6b97-8001-7dc85bcd6ee2'}}, 
#   tasks=(), 
#   interrupts=()
# )

for checkpoint_tuple in checkpointer.list(config):
    print ()
    print (checkpoint_tuple[2]["step"])
    print (checkpoint_tuple[2]["source"])
    print (checkpoint_tuple[1]["channel_values"])
    
    # print (checkpoint_tuple)
    # CheckpointTuple(
    #   config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f0baba1-356f-6ac9-8002-a8716470024c'}}, 
    #   checkpoint={
    #       'v': 4, 
    #       'ts': '2025-11-06T02:41:19.963616+00:00', 
    #       'id': '1f0baba1-356f-6ac9-8002-a8716470024c', 
    #       'channel_versions': {
    #           '__start__': '00000000000000000000000000000002.0.2059614386569527', 
    #           'foo': '00000000000000000000000000000004.0.41620864564208193', 
    #           'branch:to:node_a': '00000000000000000000000000000003.0.019600769484158453', 
    #           'bar': '00000000000000000000000000000004.0.41620864564208193', 
    #           'branch:to:node_b': '00000000000000000000000000000004.0.41620864564208193'
    #       }, 
    #       'versions_seen': {
    #           '__input__': {}, 
    #           '__start__': {'__start__': '00000000000000000000000000000001.0.3446218279751111'}, 
    #           'node_a': {'branch:to:node_a': '00000000000000000000000000000002.0.2059614386569527'}, 
    #           'node_b': {'branch:to:node_b': '00000000000000000000000000000003.0.019600769484158453'}
    #       }, 
    #       'updated_channels': ['bar', 'foo'], 
    #       'channel_values': {'foo': 'b', 'bar': ['a', 'b']}
    #   }, 
    #   metadata={
    #       'source': 'loop', 
    #       'step': 2, 
    #       'parents': {}
    #   }, 
    #   parent_config={
    #       'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f0baba1-356a-6ca6-8001-74432b19c844'}}, 
    #   pending_writes=[]
    # )