import os
from dotenv import load_dotenv
from langchain_community.llms import Tongyi

load_dotenv()
llm = Tongyi(api_key=os.getenv("bail_api_key"),base_url=os.getenv("bail_base_url"),model = "qwen-plus")

query = "以我想变成为话题，补充后面的话，要求补充的内容深刻且感人，补充内容不超过200个字"
res = llm.invoke(query)
print(res)