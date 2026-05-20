# from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import os
#
# load_dotenv()
#
# # 原始字符串模板
# template = "桌上有{number}个苹果，四个桃子和 3 本书，一共有几个水果?"
# prompt = PromptTemplate.from_template(template)
#
# # 创建模型实例
# llm = ChatOpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"),
#                  base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
#                  model='qwen-plus',
#                  temperature=0)
#
# # 创建Chain
# chain = prompt | llm
#
# # 调用Chain，返回结果
# result = chain.invoke({"number": "3"})
# print(result)


from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()


# 创建模型实例
template = PromptTemplate(
    input_variables=["role", "fruit"],
    template="{role}喜欢吃{fruit}?",
)

# 创建LLM
llm = ChatOpenAI(api_key=os.getenv("bail_api_key"),
                 base_url=os.getenv("bail_base_url"),
                 model='qwen3.6-plus',
                 temperature=0)


llm_chain = template | llm
# 输入列表
input_list = [
    {"role": "猪八戒", "fruit": "人参果"}, {"role": "孙悟空", "fruit": "仙桃"}
]
res = llm_chain.batch(input_list)
print(res[0])