from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI


load_dotenv()

LLMChain = ChatOpenAI(api_key=os.getenv("bail_api_key"),
                      base_url=os.getenv("bail_base_url"),model="qwen3.6-plus")
response = LLMChain.invoke("你好我是余小包")
print(response)


response = LLMChain.invoke("我是谁")
print(response)


