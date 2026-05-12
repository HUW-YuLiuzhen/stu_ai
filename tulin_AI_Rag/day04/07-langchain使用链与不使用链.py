# 第一种不使用链 第一步：定义提示词，第二步：创建访问模型连接 ， 第三步：创建了提示词模板，将提示词丢给了提示词模板     第四步：将提示词模板丢给模型
# 导入LangChain中的提示模板
from langchain_core.prompts import PromptTemplate
# 导入LangChain中的OpenAI模型接口
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
import os
# 原始字符串模板
template = "桌上有{number}个苹果，四个桃子和 3 本书，一共有几个水果?"
# 创建LangChain模板
prompt_temp = PromptTemplate.from_template(template)
# 根据模板创建提示
prompt = prompt_temp.format(number=2)
model = ChatOpenAI(api_key=os.getenv("bail_api_key"),
                   base_url=os.getenv("bail_base_url"),
                   model='qwen-plus')
res = model.invoke(prompt)
print(res)


# 第二种使用链   第一步：创建提示词模板，第二步：创建访问模型连接，第三步：创建了一个大预言模型店链，将模型访问和提示词组合在一起
from langchain_classic.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
# 原始字符串模板
template = "桌上有{number}个苹果，四个桃子和 3 本书，一共有几个水果?"
# 创建模型实例
llm = ChatOpenAI(api_key=os.getenv("bail_api_key"),
                 base_url=os.getenv("bail_base_url"),
                 model='qwen-max',
                 temperature=0)
# 创建LLMChain
llm_chain = LLMChain(
    prompt=PromptTemplate.from_template(template),
    llm=llm,
)
# 调用LLMChain，返回结果
result = llm_chain.invoke({"number": 2})
print(type(result))
print(result['text'])

# 第三种使用LECL链式写法
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os

load_dotenv()

# 创建提示词
prompt = ChatPromptTemplate.from_template("桌上有{number}个苹果，四个桃子和 3 本书，一共有几个水果?")

# 创建llm模型
model = ChatOpenAI(api_key=os.getenv("bail_api_key"),
                 base_url=os.getenv("bail_base_url"),
                 model='qwen-max',
                 temperature=0)
# 创建输出解释器
output_parser = StrOutputParser()
# 使用chain链在一起   __or__
# 先提示词和问题-》模型调用-》输出结果
chain = prompt | model | output_parser

print(chain.invoke({"number": "2"}))
