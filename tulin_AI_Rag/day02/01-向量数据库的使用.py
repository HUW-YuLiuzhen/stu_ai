import chromadb

# pip install chromadb
'''
第一步：创建存储
    内存存储
    本地持久化存储
第二步：存储检索的数据文本,设置数据的唯一编号
第三步：进行增删改查的操作
    
'''

# 链接向量数据库
# 默认在内存当中    内存
# client = chromadb.Client()
# 持久化存储 path地址
client = chromadb.PersistentClient(path="./chroma_db")
# get_or_create_collection 如果有集合则返回，没有则创建
cll = client.get_or_create_collection(name='test')

# print(cll)

# 添加向量   存向量    检索的数据(文本)   和 问题进行拼接
cll.add(
    documents=["Article by john", "Article by Jack", "Article by Jill"],
    embeddings=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    ids=["1", "2", "3"]
)

# 查询数据
# rest = cll.query(query_texts=["Who wrote the article?"], n_results=1)
# print(f'{rest} \n')

# print(f'{cll.get()} ')
# print('\n')
# print(cll.get(include=['embeddings']) )
#
# print('\n')
# print(cll.get(include=['documents']) )
#
# print('\n')
# print(cll.get(where_document={"$contains": "john"}))
#
# print('\n')
# # 查询数据
# aa = cll.get(include=['embeddings'], where_document={"$contains": "john"},)
# # aa = cll.get()
# print(aa)
#
# print('\n')
# # # 删除数据
# cll.delete(ids=['1'])
# print(cll.get())
#
# print('\n')
# # 查询数据
# print(cll.get(include=['documents']) )
#
# print('\n')
# # 修改数据   速度快
# cll.update(
#     documents=["Article by john", "Article by Jack", "Article by Jill"],
#     embeddings=[[10,2,3],[40,5,6],[70,8,9]],
#     ids=["1", "2", "3"])
# print(cll.get(include=["embeddings"]))