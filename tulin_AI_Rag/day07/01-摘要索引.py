
from tulin_AI_Rag.chain_llm_tools import LLM, Embedding_model
from langchain_core.stores import InMemoryByteStore
from langchain_chroma import Chroma
from langchain_community.document_loaders import UnstructuredWordDocumentLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# MultiVectorRetriever 多用检索器
from langchain_classic.retrievers import MultiVectorRetriever
import uuid
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap


'''
    1.从多个来源（Word 文档 + 网页）加载文档
    2.切分成小段（chunks）
    3.对每个 chunk 用 LLM 生成摘要
    4.把摘要存入向量数据库（用于检索）
    5.把原始文档存入文档存储（根据检索到的摘要 ID 取出原文）
    6.最后演示：用摘要检索到匹配片段，再根据 ID 拿到原始文档
'''
url = 'https://news.pku.edu.cn/mtbdnew/15ac0b3e79244efa88b03a570cbcbcaa.htm'
LoaderS = {
    UnstructuredWordDocumentLoader(file_path="人事管理流程.docx"),
    WebBaseLoader(web_path=url)
}

docs = []
# docs1 = []

for Loader in LoaderS:
    docs.extend(Loader.load())
    # docs1.append(Loader.load())

# print(f'{docs = }')
# print(f'{docs1 = }')


TextSplitter = RecursiveCharacterTextSplitter(chunk_size=1024,chunk_overlap=150)

docs = TextSplitter.split_documents(docs)

# print(docs)
Chat_Prompt = ChatPromptTemplate.from_template("请认真总结一下当前输出内容的信息{doc_text}")
# 创建摘要链
chain = (
    {"doc_text": lambda x:x.page_content}
    |Chat_Prompt
    |LLM
    |StrOutputParser()
)

# str = chain.invoke(docs,{'max_concurrency': 5})
str1 = chain.batch(docs,{'max_concurrency': 5}) # 同时调用链执行5个文档内容处理

# print(f'{str = } ,{len(str)}')
# print(f'{str1 = } ,{len(str1)}, {len(docs)} , {type(str1)} , {type(docs)}')

# 存如向量数据库
vector = Chroma(
    collection_name="str1",
    embedding_function=Embedding_model
)
# 内存键值存储，存放原始文档
store = InMemoryByteStore()
#
id_key = "doc_id"
# 创建多用检索器
Retriever = MultiVectorRetriever(
    vectorstore=vector,
    byte_store = store,
    id_key = id_key
)
# 根据列表长度生成对应输了随机id
doc_ids = [str(uuid.uuid4()) for i in str1]

# print(f'{doc_ids = },{len(doc_ids)} , {type(doc_ids)}')

strip_docs = [
    Document(page_content=str,metadata={id_key:doc_ids[t]}) for t,str in enumerate(str1)
]

# print(f'{strip_docs = },{len(strip_docs)} , {type(strip_docs)}')

# 把压缩之后的内容添加到向量数据库
Retriever.vectorstore.add_documents(strip_docs)

# 源文档加载到内容
Retriever.docstore.mset(list(zip(doc_ids,docs)))

# 下面建立测试
prompt = ChatPromptTemplate.from_template("根据下面的文档回答问题:\n\n{doc}\n\n问题: {question}")
# 生成问题回答链
chain_query = RunnableMap({
    "doc": lambda x: Retriever.invoke(x["question"]),
    "question": lambda x: x["question"]
}) | prompt | LLM | StrOutputParser()

# 生成问题回答
# query = "聘用原则是什么？"
# answer = chain_query.invoke({"question": query})
# print("-------------回答--------------")
# print(answer)
#
# retrieved_docs = Retriever.invoke(query)
# print("-------------检索到的文档--------------")
# print(retrieved_docs)



sub_docs = Retriever.vectorstore.similarity_search("聘用原则是什么？")
print(sub_docs)
print("-------------检索到的文档--------------")
print(sub_docs[0])

summ_id = sub_docs[0].metadata[id_key]

orig_doc = Retriever.docstore.mget([summ_id])
print("-------------原始文档--------------")
print(orig_doc)