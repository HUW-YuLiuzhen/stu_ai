# 这是一个概念性代码示例，需要你安装 langchain, openai, faiss-cpu 等库才能运行
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
# 假设你已经配置好了OpenAI API Key
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv(verbose=True)


# 1. 准备你的知识库文本
knowledge_text = """
RAG全称是检索增强生成，是解决大模型幻觉与知识滞后的核心方案。
RAG主要分为索引和推理两个阶段。
索引阶段：文档加载、文本切块、向量化、存入向量数据库。
推理阶段：问题向量化、相似度检索、上下文拼接、大模型生成答案。
"""

# 2. 文本切块
# chunk_size是每个块的大小，chunk_overlap是块与块之间的重叠部分，防止信息被切断
text_splitter = CharacterTextSplitter(chunk_size=50, chunk_overlap=10)
docs = [Document(page_content=knowledge_text)]
split_docs = text_splitter.split_documents(docs)

# 3. 构建向量库
# 这里使用FAISS，一个轻量级的本地向量库，非常适合新手入门
embedding_model = OpenAIEmbeddings() # 使用OpenAI的嵌入模型
vector_store = FAISS.from_documents(split_docs, embedding_model)

# 4. 设置检索器
retriever = vector_store.as_retriever(search_kwargs={"k": 2}) # 每次检索最相关的2个片段

# 5. 定义提示词模板
# 这个模板告诉大模型：只能根据我给你的上下文来回答，不要瞎编
rag_prompt = PromptTemplate.from_template("""
请严格根据下方的参考上下文来回答问题。如果上下文中没有答案，请直接说“我不知道”，禁止编造任何内容。
参考上下文：
{context}

用户问题：
{question}
""")

# 6. 组装RAG链路
llm = ChatOpenAI(temperature=0) # temperature=0让模型输出更确定、更客观
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# 7. 测试
question = "RAG包含哪两个核心阶段？"
res = rag_chain.invoke(question)
print("RAG智能回答：", res)