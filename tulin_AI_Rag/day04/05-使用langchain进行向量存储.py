import os
from dotenv import load_dotenv
# 向量数据库
from  langchain_chroma import Chroma
# 本地模型加载
# from sentence_transformers import SentenceTransformer
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
# 文档加载
from  langchain_community.document_loaders import PyPDFLoader
# 文本分割
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()

# 加载文档
pdf_load = PyPDFLoader(f'财务管理文档.pdf')
# 设置分割器
pdf_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 30,
    length_function = len,
    separators = ["\n", " ", ""]
)
# 加载文档
doc_pdf = pdf_load.load_and_split()
# # 进行文档切割
doc_list = []
for docs in doc_pdf:
    doc_list.append(docs.page_content)
# print(type(doc_list))
document_splitter = pdf_splitter.split_documents(doc_pdf)
# print(type(document_splitter))
# 创建连接本地向量数据库逻辑,这个方法封装了将文本转换为向量的逻辑
embs = HuggingFaceEmbeddings(model_name=r"G:\locahost_llm\nlp_gte_sentence-embedding_chinese-small\iic\nlp_gte_sentence-embedding_chinese-small")
# 验证创建向量是否正常
# print(embs.embed_query("我爱学习"))
# 创建连接Chroma的方法
persist_directory=r"Chroma_db"
db_chroma = Chroma.from_documents(
    documents=document_splitter,
    embedding=embs,
    persist_directory=persist_directory
)
# 检索
resource = db_chroma.similarity_search("财务管理制度")
print(resource)
for doc in resource:
    print(f"{doc}\n-------\n")
