# pip install langchain-text-splitters
# RecursiveCharacterTextSplitter (递归字符文本切分器)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.pdf import PyPDFLoader
# 创建加载pdf容器
pdf_loader = PyPDFLoader(f'财务管理文档.pdf')
docf_ld = pdf_loader.load()
print(f'{docf_ld = }')
dg_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,      # 每个块的最大长度（字符数）
    chunk_overlap=20,    # 块之间的重叠字符数，用于避免语义断裂
    length_function=len, # 计算长度的方法
    separators=["\n\n", "\n", " ", ""] # 可选，自定义分隔符优先级
)
# 分割文档
docf = dg_splitter.split_documents(docf_ld)
print(f'{docf = } ： {type(docf)} ')

# 分割字符串
for doc_txt in docf:
    doct = dg_splitter.split_text(doc_txt.page_content)
    # print(f'{doct = } :  {type(doct)}')

# 另外一种切割方式
docf_splitter = pdf_loader.load_and_split()
# print(f'{docf_splitter = }')
new_docf = dg_splitter.split_documents(docf_splitter)
print(f'{new_docf = } : {type(new_docf)} ')


