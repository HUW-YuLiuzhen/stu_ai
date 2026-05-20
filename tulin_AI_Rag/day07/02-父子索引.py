#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from tulin_AI_Rag.chain_llm_tools import LLM, Embedding_model
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_core.stores import BaseStore, InMemoryByteStore
from langchain_core.documents import Document
import pymysql
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap
from langchain_core.output_parsers import StrOutputParser



# 目标 URL
url = "https://news.pku.edu.cn/mtbdnew/15ac0b3e79244efa88b03a570cbcbcaa.htm"

# 加载网页
loader = WebBaseLoader(url)
docs = loader.load()

# 创建主文档分割器
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)

# 创建子文档分割器  多少个子文档     5个   0-400    200-600   400-800   600-1000
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

# 创建向量数据库对象
vectorstore = Chroma(collection_name="split_parents", embedding_function=Embedding_model,persist_directory="chroma_data")



# 自定义 MySQL Store
class MySQLStore(BaseStore):
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',  # 添加字符集支持
            cursorclass=pymysql.cursors.DictCursor
        )
        self._create_table()

    def _create_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    doc_id VARCHAR(255) PRIMARY KEY,
                    page_content LONGTEXT,
                    metadata LONGTEXT
                )
            """)
            self.connection.commit()

    def mset(self, key_value_pairs):
        with self.connection.cursor() as cursor:
            for key, doc in key_value_pairs:
                metadata = json.dumps(doc.metadata) if doc.metadata else "{}"
                cursor.execute("""
                    INSERT INTO documents (doc_id, page_content, metadata)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE page_content=%s, metadata=%s
                """, (key, doc.page_content, metadata, doc.page_content, metadata))
            self.connection.commit()

    def mget(self, keys):
        with self.connection.cursor() as cursor:
            if not keys:
                return []
            placeholders = ", ".join(["%s"] * len(keys))
            cursor.execute(f"SELECT doc_id, page_content, metadata FROM documents WHERE doc_id IN ({placeholders})",
                           keys)
            results = cursor.fetchall()
            return [Document(page_content=row["page_content"],
                             metadata=json.loads(row["metadata"]) if row["metadata"] else {}) for row in results]

    def mdelete(self, keys):
        with self.connection.cursor() as cursor:
            if not keys:
                return
            placeholders = ", ".join(["%s"] * len(keys))
            cursor.execute(f"DELETE FROM documents WHERE doc_id IN ({placeholders})", keys)
            self.connection.commit()

    def yield_keys(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT doc_id FROM documents")
            for row in cursor.fetchall():
                yield row["doc_id"]

    def close(self):
        self.connection.close()


# 创建 MySQL 存储对象
store = MySQLStore(host="localhost", user="root", password="root", database="langchain_db")

# 存在内存当中
# store = InMemoryByteStore()

# 创建父文档检索器
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
    search_kwargs={"k": 1},
)

# 添加文档
retriever.add_documents(docs)

print('父文档存储数量:', len(list(store.yield_keys())))


# 创建 prompt 模板
# template = """请根据下面给出的上下文来回答问题:
# {context}
# 问题: {question}
# """
#
# # 由模板生成 prompt
# prompt = ChatPromptTemplate.from_template(template)
#
# # # 创建 chain
# chain = RunnableMap({
#     "context": lambda x: retriever.invoke(x["question"]),
#     "question": lambda x: x["question"]
# }) | prompt | LLM | StrOutputParser()
#
# print("------------模型回复------------------------")
#
# response = chain.invoke({"question": "天才AI少女是谁？"})
# print(response)

# 在向量数据库中检索  得到的子文档
# sub_docs = vectorstore.similarity_search("天才AI少女是谁？", k=1)
# print("------------检索到的子文档------------------------")
# print(sub_docs)
#
# ret_docs = retriever.invoke("天才AI少女是谁？")
# print("------------检索到的父文档------------------------")
# print(ret_docs)







