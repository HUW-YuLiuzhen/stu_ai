#!/usr/bin/env python
# -*- coding: UTF-8 -*-


# 加载所需的库
import os

# from langchain import hub
from langsmith import Client

from langchain_tavily import TavilySearch
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# from langchain.tools.retriever import create_retriever_tool
from langchain_core.tools.retriever import create_retriever_tool
load_dotenv()

# 查询 Tavily 搜索 API 并返回 json 的工具
search = TavilySearch(tavily_api_key=os.getenv("TAVILY_API_KEY"))
# # 执行查询
# res = search.invoke("目前市场上苹果手机16的售价是多少？")
# print(res)


# 创建索引器根据上述查询的结果

# 加载HTML内容为一个文档对象
loader = WebBaseLoader("https://news.qq.com/rain/a/20240920A07Y5Y00")
# 读取文档
docs = loader.load()
# print(docs)


# 分割文档
documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)

# 向量化
vector = FAISS.from_documents(documents, DashScopeEmbeddings(dashscope_api_key=os.getenv('DASHSCOPE_API_KEY')))

# 创建检索器
retriever = vector.as_retriever()

# print(retriever.invoke("目前市场上苹果手机16的售价是多少？"))

# 创建检索工具
retriever_tool = create_retriever_tool(
    retriever,
    "iPhone_price_search",
    "当前工具用于查询苹果16手机的售价, 其他任何版本都不能使用此工具, 苹果17不能使用此工具",
)

tools = [search, retriever_tool]

# 初始化大模型
# 模型版本
#
llm = ChatOpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"),
                 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                 model='qwen-max', temperature=0)
hub = Client()
prompt = hub.pull_prompt("hwchase17/openai-functions-agent")
# 打印Prompt
# print(prompt)

# from langchain.agents import create_openai_functions_agent
from langchain_classic.agents import create_openai_functions_agent


agent = create_openai_functions_agent(llm, tools, prompt)

from langchain_classic.agents import AgentExecutor

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# print(agent_executor.invoke({'input':"目前市场上苹果手机16的售价是多少？"}))
print(agent_executor.invoke({'input':"目前市场上苹果17的售价是多少？"}))
# print(agent_executor.invoke({'input': "2024年美国总统谁选上了"}))






