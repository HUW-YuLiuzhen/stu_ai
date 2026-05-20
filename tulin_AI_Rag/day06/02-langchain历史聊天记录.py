from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory



load_dotenv()
LLMChain = ChatOpenAI(api_key=os.getenv("bail_api_key"),
                      base_url=os.getenv("bail_base_url"),model="qwen3.6-plus")

History = ChatMessageHistory()
History.add_user_message("你好啊")
History.add_ai_message("你好我是你的智能助手琪琪同学")
History.add_ai_message("请问有什么需要帮助的吗")
History.add_user_message("没有退下吧")

# print(History.messages)

resource = LLMChain.invoke(History.messages)
print(resource)

resource = LLMChain.invoke("你是谁")
print(resource)


