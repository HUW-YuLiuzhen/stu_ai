import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

load_dotenv()
# 第一步创建本地向量数据库的连接
client_emb = HuggingFaceEmbeddings(model_name=r"G:\locahost_llm\nlp_gte_sentence-embedding_chinese-small\iic\nlp_gte_sentence-embedding_chinese-small")
print(f"加载本地嵌入模型成功")
# 加载本地向量数据库
# 定义本地向量数据库地址
persist_directory_path = r"Chroma_db"
# 加载本地向量数据库
db_chroma = Chroma(
    persist_directory=persist_directory_path,
    embedding_function=client_emb
)
print("本地向量数据库加载完成***************************")
resource = db_chroma.as_retriever(search_kwargs={"k":8})
print("检索器创建完成***************************")
HumanMessage = resource.invoke("我想知道你的基础信息")
# print(f'{type(HumanMessage)}:{HumanMessage}')
messages_list = []
replace_old = r"\n"
replace_old1 = r"\n \n"
for i,message in enumerate(HumanMessage):
    messages_list.append(f'第{i+1}行：{message.page_content.replace(replace_old,"").replace(replace_old1,"")}')
print(messages_list)
