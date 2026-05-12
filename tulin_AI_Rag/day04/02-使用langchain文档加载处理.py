# pip install pypdf
# 加载pdf
from langchain_community.document_loaders.pdf import PyPDFLoader
# 创建加载pdf容器
pdf_loader = PyPDFLoader(f'财务管理文档.pdf')
docf = pdf_loader.load()
# print(f'{docf = }')


# 加载word
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
doc_loader = UnstructuredWordDocumentLoader(f'人事管理流程.docx')
docw = doc_loader.load()
# print(f'{docw = }')

# 加载excle
# pip install pandas
# pip install msoffcrypto-tool
# pip install openpyxl
from langchain_community.document_loaders import UnstructuredExcelLoader
excle_loader = UnstructuredExcelLoader(f'小白瘦身饮食计划.xlsx')
excle = excle_loader.load()
# print(f'{excle = }')

# 加载txt
from langchain_community.document_loaders import TextLoader
txt_loader = TextLoader("example.txt", encoding="utf-8")  # 替换为你的 TXT 文件路径
txt_docs = txt_loader.load()
# print(txt_docs)

# 加载在线的pdf
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("https://arxiv.org/pdf/2302.03803.pdf")
data = loader.load()
# print(data)
# 加载在线的pdf
# pip install unstructured pdf2image opencv-python pikepdf
# pip install pi_heif
# pip install unstructured-inference
from langchain_community.document_loaders import OnlinePDFLoader
# 替换为在线 PDF 的直接链接（例如 arXiv 上的论文）
pdf_url = "https://arxiv.org/pdf/2307.09288.pdf"
loader = OnlinePDFLoader(pdf_url)
docs = loader.load()
print(docs)



# 加载静态网页的内容
from langchain_community.document_loaders import WebBaseLoader
WebBaseLoader = WebBaseLoader(f"https://www.gov.cn/zhengce/content/202510/content_7043916.htm")
web_docs = WebBaseLoader.load()
# print(web_docs)


