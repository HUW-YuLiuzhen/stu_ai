import os
# 0.3版本能进行导入 替换导入方式
# from langchain.chains.combine_documents import create_stuff_documents_chain
# langchain_classic 提供向下兼容模块
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_classic.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from dotenv import load_dotenv

# 用户问题 → 向量检索 → 构建新的提示词 → LLM生成答案 → 输出结果
#  这里需要注意
# 初始化本地文件
load_dotenv()

# 定义获取本地向量数据库内容
faiss_path = 'faiss_db'

# 创建一个embedding模型
embs = DashScopeEmbeddings(dashscope_api_key=os.getenv('bail_api_key'),model='text-embedding-v4')

# 创建获取本地向量数据的连接
vector_store = FAISS.load_local(folder_path=faiss_path,embeddings=embs,allow_dangerous_deserialization=True)  # 允许加载 pickle 文件（仅限可信文件）

# 创建一个提示词模板
prompt = ChatPromptTemplate.from_template("""仅根据提供的上下文回答以下问题:

<context>
{context}
</context>

问题: {input}""")

# 创建大语言模型
llm = ChatOpenAI(api_key=os.getenv('bail_api_key'),base_url=os.getenv('bail_base_url'),model='qwen3.6-plus')

# create_stuff_documents_chain  把拼接好的提示词  给大模型
# from langchain_core.prompts.chat import
doc_chain = create_stuff_documents_chain(llm, prompt)
# print(f'{doc_chain = }')

# 创建检索器  把检索的功能进行封装  as_retriever最基础的检索器
retr = vector_store.as_retriever()
# print(f'{retr = }')

# 把检索到的数据  给到 doc_chain
# from langchain_community.vectorstores.faiss import
res_chain = create_retrieval_chain(retr, doc_chain)
print(f'{res_chain = }')
#
# from openai.resources.chat.completions.completions import
res = res_chain.invoke({"input":"密云水库水源保护条例什么时候执行"})
print(res)

