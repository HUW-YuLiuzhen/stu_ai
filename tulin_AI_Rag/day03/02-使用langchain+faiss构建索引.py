import os
# 加载网页资源
import bs4
# 1.0版本的导入  pip 下载
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 老版本的导入方法
# from langchain.text_splits import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
# 千问的向量模型加载库
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()

# 第一步初始化一个静态加载，获取网页指定内容
# 第二步 将内容进行分割
# 第三步 将内容向量化
# 第四步 将向量化内容存储到faiss向量数据库中
# 第一步
load = WebBaseLoader(web_paths=("https://www.gov.cn/zhengce/content/202510/content_7043916.htm",),bs_kwargs=dict(
        parse_only=bs4.SoupStrainer( id=("UCAP-CONTENT"))))
docs = load.load()

# 第二步
splits = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
split_docs = splits.split_documents(docs)
print(f'{len(split_docs)} , {type(split_docs)} , {split_docs = } ')

# 第三步
embs = DashScopeEmbeddings(dashscope_api_key=os.getenv('bail_api_key'),model='text-embedding-v4')

base_size = 5
vect = None
# 初始化faiss
# 切割文档每5个一组
for doc in range(0,len(split_docs),base_size):
        batch_docs = split_docs[doc:doc + base_size]
        # print(f'{doc} - {doc+base_size} : {batch_docs} \n' )
        # print(f'第{doc // base_size + 1}批次 文档数量: {len(batch_docs)}')
        if doc == 0:
                vect = FAISS.from_documents(batch_docs, embs)
        else:
                # new_vect = FAISS.from_documents(batch_docs, embs)
                # vect.merge_from(new_vect)
                vect.add_documents(batch_docs)

        print(vect)

vect.save_local('faiss_db')

# 测试查询，看是否能召回相关内容
query = "密云水库水源保护条例"  # 替换成你关心的关键词
results = vect.similarity_search(query, k=3)  # 返回前3个最相似的文档

# print(results)

print(f"\n查询 '{query}' 的检索结果:")
for i, doc in enumerate(results):
    print(f"\n--- 结果 {i+1} ---")
    print(f"内容预览: {doc.page_content[:200]}...")  # 只显示前200字符
    print(f"元数据: {doc.metadata}")
