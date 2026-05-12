import os
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
load_dotenv()

ENDPOINT_URL = "Qwen/Qwen3-8B"
# ENDPOINT_URL = "deepseek-ai/DeepSeek-R1"
api_key = os.getenv('hg_api_key1')


llm = HuggingFaceEndpoint(
    endpoint_url=ENDPOINT_URL,
    huggingfacehub_api_token=api_key,  # 这个参数名是正确的
    task="text-generation",  # 添加任务类型
    max_new_tokens=512,  # 添加一些常用参数
    temperature=0.7
)

# 生成key时需要把权限都点上
chat_model = ChatHuggingFace(llm=llm)
resp = chat_model.invoke("你是谁")
# print(resp)