from langchain_core.prompts import ChatPromptTemplate
# 导入LangChain中的ChatOpenAI模型接口
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv


load_dotenv(verbose=True)
# prompt_template = "你是一个数学专家，你擅长进行数学计算"
prompt_template = "你是一个特别牛逼的{sf}技术专家，目前要求你整理一份{text},100字以内"
new_prompt = ChatPromptTemplate([
                ("system", prompt_template),
                ("human", "{text1}"),
            ])
print(new_prompt)
# messages = new_prompt.format_prompt(text1="我今年18岁，我的舅舅今年38岁，我的爷爷今年72岁，我和舅舅一共多少岁了？")
messages = new_prompt.format_prompt(sf="语言",text="介绍",text1="你简单讲一下python")
model = ChatOpenAI(api_key=os.getenv('bail_api_key'),base_url=os.getenv('bail_base_url'),model='qwen3.6-plus')
res = model.invoke(messages)
print(res.content)
print(res)


