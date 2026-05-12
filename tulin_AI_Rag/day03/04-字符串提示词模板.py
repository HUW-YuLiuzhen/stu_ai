from langchain_openai import ChatOpenAI
# 导入LangChain中的提示模板
from langchain_core.prompts  import PromptTemplate
import os
from dotenv import load_dotenv


load_dotenv()

# 创建模型实例
model = ChatOpenAI(api_key=os.getenv("bail_api_key"),
                   base_url=os.getenv("bail_base_url"),
                   model='qwen3.6-plus')

prompt = PromptTemplate(
    template="您是一位专业的程序员。\n对于信息 {text1} 进行简短描述"
)

aa = "您是一位专业的程序员。\n对于信息 {text2} 进行简短描述"
inputs1 = aa.format(text2="langchain")
print(inputs1)
oup = model.invoke(inputs1)
print(f'{oup = }')

inputs = prompt.format(text1="langchain")
print(inputs)
oup1 = model.invoke(inputs).content
print(f'{oup1 = }')