import os
from dotenv import load_dotenv
from langchain.chat_models import  init_chat_model

load_dotenv(verbose=True)

# 初始化连接
# llm = init_chat_model(
#     model='deepseek-reasoner',
#     api_key=os.getenv('ds_api_key'),
#     base_url=os.getenv('ds_base_url'),
# )
#
# res = llm.invoke("你是谁")
# print(res)
#
# from langchain_openai import ChatOpenAI
# llm1 = ChatOpenAI(api_key=os.getenv('ds_api_key'),base_url=os.getenv('ds_base_url'),model='deepseek-reasoner')
# res1 = llm1.invoke("你是谁")
# print(res1)


from langchain_deepseek import ChatDeepSeek
llm = ChatDeepSeek(
    api_key=os.getenv("ds_api_key"),
    base_url=os.getenv("ds_base_url"),
    model="deepseek-reasoner"
)

response = llm.invoke("你是谁")
print(response)
print("=" * 50)
print(response.content)

