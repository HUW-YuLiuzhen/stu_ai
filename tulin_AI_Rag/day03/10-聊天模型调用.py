import  os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()
llm = ChatTongyi(api_key=os.getenv("bail_api_key"),base_url=os.getenv("bail_base_url"),model = "qwen3.6-plus")

# query = "以我想变成为话题，补充后面的话，要求补充的内容深刻且感人，补充内容不超过200个字"
# res = llm.invoke(query)
# print(res)

# 聊天模型支持多个消息作为输入
hm = HumanMessage("你是谁")
res = llm.invoke([hm])
print(res)
print('*'*50)
sys = SystemMessage("你是历史上的诗鬼，大文豪")
res1 = llm.invoke([sys])
print(f'{res1 = } ')
print('*'*50)
message = [sys,hm]
res2 = llm.invoke(message)
print(res2)