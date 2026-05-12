import os
from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings

load_dotenv(verbose=True)
Embs = DashScopeEmbeddings(dashscope_api_key=os.getenv("bail_api_key"),model = "text-embedding-v4")

querys = ['你好','世界']
# 将输入内容向量话
res = Embs.embed_documents(querys)
print(f'{res = }')
# 请求问题向量话
res1 = Embs.embed_query("你好")
print(res1)
