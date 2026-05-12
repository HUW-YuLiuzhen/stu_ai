from langchain_community.embeddings import DashScopeEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()
# 创建连接
# 设置使用模型
embs = DashScopeEmbeddings(dashscope_api_key=os.getenv("bail_api_key"),model="text-embedding-v4")
# 不设置使用模型 默认text-embedding-v1
# embs = DashScopeEmbeddings(dashscope_api_key=os.getenv("bail_api_key"))
messages = ["你好","我是","爱你"]
# print(f'{messages = } : {type(messages)}')
# 文档的向量化`embed_documents`，接收的参数是字符串数组
res = embs.embed_documents(messages)
# print(f'{res = } : {len(res)} : {len(res[0])} ： {len(res[1])} ： {len(res[2])} ')
# 句子的向量化`embed_query`，接收的参数是字符串
query_messages = "你好"
query_res = embs.embed_query(query_messages)
print(query_res)
