import os
from email.headerregistry import MessageIDHeader

from dotenv import load_dotenv
# 导入langchain聊天模板
from langchain_core.prompts import ChatPromptTemplate
# 导入模型连接包
from langchain_openai import ChatOpenAI
# 创建解析器
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser, XMLOutputParser
from langchain_classic.chains import LLMChain  # 新增：导入 LLMChain 用于非 LCEL 链式调用

# 加载配置
load_dotenv()
# 创建模型连接
llm = ChatOpenAI(api_key=os.getenv("bail_api_key"),base_url=os.getenv("bail_base_url"),model="qwen3.6-plus")
# 创建解析器
JsonOutputParser = JsonOutputParser()
StrOutputParser = StrOutputParser()
XMLOutputParser = XMLOutputParser()

# 定义提示词模板
Prompt = ChatPromptTemplate([
    ("system","你是一个专业的开发人员"),
    ("human","{text}"),
])

# 常规调用模型
Message = Prompt.format_prompt(text="我需要妳解释一下什么是LCEL和chain的区别，用中文解释")
print(Message)
# resource = llm.invoke(Message)
# print(resource.content.replace("\n",''))

# 创建 chain 非LCEL调用方式
# Chain = LLMChain(
#     prompt=Prompt,
#     llm=llm,
#     output_parser=JsonOutputParser  # 指定输出解析器
# )
#
Chain = Prompt | llm | StrOutputParser

res = Chain.invoke({"text":"我需要妳解释一下什么是LCEL和chain的区别"})
print(res)

