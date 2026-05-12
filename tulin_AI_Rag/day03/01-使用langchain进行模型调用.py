from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
mclient = ChatOpenAI(base_url=os.getenv("bail_base_url"),api_key=os.getenv("bail_api_key"),model="qwen3.6-plus")
query = "你是什么模型有什么作用"
res = mclient.invoke(query)
print(res)
