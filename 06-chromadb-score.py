from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# 嵌入模型： 
embedding=OllamaEmbeddings(model="qwen3-embedding:4b")

# 评分方式
score_measures=[
    "default", # default = 'l2'
    "cosine",  # 用两个向量的夹角度量相似度， 1-cos(角度) 0-2
    "l2",      # 用两个向量的距离度量相似度，
    "ip"       # 用两个向量的内积/点积度量相似度， 和 cosine 接近
]

# 创建向量库和4个collection
persist_dir="./chroma_score_db"
vector_stores=[]
for score_measure in score_measures:
    collection_metadata={"hnsw:space": score_measure}
    if score_measure == "default":
        collection_metadata=None
    
    collection_name = f"my_collection_{score_measure}"
    vector_stores.append(Chroma(
        collection_name=collection_name,
        embedding_function=embedding,
        persist_directory=persist_dir,
        collection_metadata=collection_metadata
    ))

def indexing(docs):
    print ("\n加入文档：")
    for vector_store in vector_stores:
        ids=vector_store.add_documents(docs)
        print(f"\n集合：{vector_store._collection.name}")
        print (ids)

def query_with_score(query):
    for i in range(len(score_measures)):
        results=vector_stores[i].similarity_search_with_score(query)
        print (f"\n搜索：{query}")
        for doc, score in results:
            print (doc.page_content, end='\t')
            print (f"{score_measures[i]}: {score}")


# docs=[
#     Document(page_content="这个小米手机很好用"),
#     Document(page_content="我国陕西地区盛产小米"),
# ]

# indexing(docs)

query_with_score("雷军最近有点烦")