from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# 嵌入模型
embedding=OllamaEmbeddings(model="nomic-embed-text")

# 向量库（知识库）
vector_store=Chroma(
    collection_name="example_collection",
    embedding_function=embedding,
    persist_directory="./chroma_langchain_db"
)

# 相似度查询
results = vector_store.similarity_search(
    "What imitations dose Force-aware have?"
)

for index, result in enumerate(results):
    print (index)
    print (result.page_content[:100])

# 带分数的相似度查询
results = vector_store.similarity_search_with_score(
    "What imitations dose Force-aware have?"
)

for doc,score in results:   # unpacking
    print (score)
    print (doc.page_content[:100])


# 用向量进行相似度查询
print ("用向量进行相似度查询")
vector = embedding.embed_query(
    "What imitations dose Force-aware have?"
)

results = vector_store.similarity_search_by_vector(
    vector
)

for index, result in enumerate(results):
    print (index)
    print (result.page_content[:100])


# 0.5039341449737549
# adjustments. This approach supports diverse behaviors like position tracking, force application, and
# 0.5104950666427612
# commands, estimated end-effector contact forces, and RGB images from cameras mounted on both
# the end
# 0.5420910120010376
# tion C. Policy learning is supervised by rewarding accurate tracking of the target end-effector posi
# 0.5428466200828552
# (a)
# (b)
# (c)
# Figure 4:Force-aware imitation learning.(a) Time-series outputs of position and force co


# chain: langchain: 大模型，提示词模板，toots，output，Runnable 
print ("用检索器进行相似度查询")
from typing import List

from langchain_core.documents import Document
from langchain_core.runnables import chain

@chain
def retriever(query: str) -> List[Document]:
    return vector_store.similarity_search(query, k=1)

results = retriever.invoke("What imitations dose Force-aware have?")
for index, result in enumerate(results):
    print (index)
    print (result.page_content[:100])