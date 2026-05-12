import json
import chromadb
import hashlib
from openai import OpenAI
from dotenv import load_dotenv
import os

'''
chroma学习：<https://zhuanlan.zhihu.com/p/680661442> 


结合chromadb 构建自己的医疗知识库
第一步 创建本地化持久存储
第二步 解析文档进行索引话
    创建模型连接方法
    创建文本向量化操作
    创建文档
'''

class MylocahostDBbase:
    def __init__(self,testName):
        # 本地持久化
        mclient = chromadb.PersistentClient(path="./chroma_db1")
        # cosin 计算
        self.collection = mclient.get_or_create_collection(
            name=testName,
            metadata={"hnsw:space": "cosine"}
        )
    # 文本向量化
    def get_embedding(self,text,model,ct):
        data = ct.embeddings.create(input=text, model=model)
        return [x.embedding for x in data.data]
    # 连接模型方法
    def gettoenv(self):
        load_dotenv()
        client = OpenAI(api_key=os.getenv('bail_api_key'), base_url=os.getenv('bail_base_url'))
        return client

    def getModel(self):
        md = "text-embedding-v4"
        return md

    # 创建文档解析方法，将问题和回答存入到向量数据库中
    def add_documents(self,instructions,outputs):
        clt = self.gettoenv()
        model = self.getModel()
        combined_texts = [f"问题：{inst} 回答：{out}" for inst, out in zip(instructions, outputs)]
        embs = self.get_embedding(combined_texts, model, clt)
        ids = []
        for i, text in enumerate(combined_texts):
            # 使用内容的前50个字符+索引作为哈希种子，防止极端的哈希碰撞
            unique_str = f"{i}_{text[:50]}"
            hash_id = hashlib.md5(unique_str.encode('utf-8')).hexdigest()
            ids.append(hash_id)
        self.collection.add(
            documents=outputs,
            embeddings=embs,
            ids=ids,
            metadatas = [{"source_question": inst} for inst in instructions]
        )
        print(f"成功导入 {len(ids)} 条数据")

    def search(self, query,model,ct,n_results=3):
        query_emb = self.get_embedding([query], model, ct)
        res = self.collection.query(
            query_embeddings=query_emb,
            n_results=n_results,
            include=["documents", "metadatas", "distances"]  # 获取更多信息
        )
        return res

if __name__ == '__main__':
    with open('train_zh.json', 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]

    # print(data)
    # print("\n")
    # print(data[0:100])

    # 获取前10条的问题和输出
    instructions = [entry['instruction'] for entry in data[0:10]]
    outputs = [entry['output'] for entry in data[0:10]]

    # combined_texts = [f"问题：{inst} 回答：{out}" for inst, out in zip(instructions, outputs)]

    # 创建一个向量数据库对象
    vector_db = MylocahostDBbase("demo")
    vector_db.add_documents(instructions, outputs)

    query = "每次都会拉大便"
    model = vector_db.getModel()
    ct = vector_db.gettoenv()
    res = vector_db.search(query,model,ct)
    print(f"\n用户提问: {query}")
    print("-" * 30)
    for i, doc in enumerate(res['documents'][0]):
        # 1. 获取 ID (从 res['ids'] 中获取)
        matched_id = res['ids'][0][i]

        # 2. 获取元数据
        source_q = res['metadatas'][0][i]['source_question']

        # 3. 打印详细信息
        print(f"[匹配 {i + 1}] ID: {matched_id}")  # 这里打印了 Hash ID
        print(f"来源问题: {source_q}")
        print(f"回答: {doc}")
        print(f"距离: {res['distances'][0][i]}")
        print("-" * 30)