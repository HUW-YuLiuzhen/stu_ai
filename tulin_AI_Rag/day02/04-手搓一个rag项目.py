'''
    实现rag： 索引    检索    生成答案
        索引：
            第一步文档拆分
            第二步内容向量化
        检索：
            第一步：设置好提示词模板
            第二步：根据问题检索内容
            第三步：将问题和检索内容拼接为一个新的提示词模板
        生成答案：
            根据新的提示词模板 调用模型生成内容
'''

# 先下载解析PDF和word的模块
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple python-docx
# 操作文档 https://blog.csdn.net/PolarisRisingWar/article/details/147332412
# pip  install -i https://pypi.tuna.tsinghua.edu.cn/simple pdfminer.six
# 使用文档  https://www.jb51.net/python/335075me6.htm

import json
import chromadb
import hashlib
from openai import OpenAI
from dotenv import load_dotenv
import os
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer


# 第一步
# 拆分文档，内容切割
class readPdf_split:
    def __init__(self, pdf_path):
        self.loca_path = pdf_path

    # 按照固定字符切割文档
    def sliding_window_chunks(self,text, chunk_size, stride):
        return [text[i:i + chunk_size] for i in range(0, len(text), stride)]

    def open_pdf(self,page_numbers=None):
        '''从 PDF 文件中（按指定页码）提取文字'''
        full_text = ''
        # 提取全部文本
        # print(extract_pages(self.loca_path))
        for i, page_layout in enumerate(extract_pages(self.loca_path)):
        #     # 如果指定了页码范围，跳过范围外的页
        #         print(f'第 {i+1} 行：输出内容为：{page_layout}')
            if page_numbers is not None and i not in page_numbers:
                continue
            for element in page_layout:
                # print(element)
        #       # 检查element是不是文本
                if isinstance(element, LTTextContainer):
                    # print(element.get_text())
        #             # 将换行和空格去掉
                    full_text += element.get_text().replace("\n", "").replace(" ", "")
        # print(f'{full_text = }')

        text_chunks = self.sliding_window_chunks(full_text, 250, 100)
        return text_chunks

# 解析内容存入向量数据库中
class MylocahostDBbase:
    def __init__(self, testName):
        # 本地持久化
        self.name = testName
        mclient = chromadb.PersistentClient(path="./chroma_db3")
        # cosin 计算
        self.collection = mclient.get_or_create_collection(
            name=self.name,
            # metadata={"hnsw:space": "cosine"}
        )

    # 文本向量化
    def get_embedding(self, text, model, ct):
        data = ct.embeddings.create(input=text, model=model)
        return [x.embedding for x in data.data]

    def get_embedding_batch(self, texts, model, ct, batch_size):
        """分批获取embedding，每批最多10个文本"""
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                data = ct.embeddings.create(input=batch, model=model)
                all_embeddings.extend([x.embedding for x in data.data])
                print(f"已处理 {min(i+batch_size, len(texts))}/{len(texts)} 条")
            except Exception as e:
                print(f"处理批次 {i//batch_size + 1} 时出错: {e}")
                # 如果批次失败，尝试单个处理
                for text in batch:
                    try:
                        data = ct.embeddings.create(input=[text], model=model)
                        all_embeddings.extend([x.embedding for x in data.data])
                    except Exception as e2:
                        print(f"处理单个文本失败: {e2}")
                        all_embeddings.append(None)
        return all_embeddings


    # 连接模型方法
    def gettoenv(self):
        load_dotenv()
        client = OpenAI(api_key=os.getenv('bail_api_key'), base_url=os.getenv('bail_base_url'))
        return client

    def getModel(self):
        md = "text-embedding-v4"
        return md

    # 创建文档解析方法，将问题和回答存入到向量数据库中
    def add_documents(self, datas):
        clt = self.gettoenv()
        model = self.getModel()
        # combined_texts = [f"问题：{inst} 回答：{out}" for inst, out in zip(instructions, outputs)]
        # 传入少量数据进行向量化
        # embs = self.get_embedding(datas, model, clt)
        embs = self.get_embedding_batch(datas, model, clt,10)
        # print(embs)

        ids = []
        for i, text in enumerate(embs):
            # 使用内容的前50个字符+索引作为哈希种子，防止极端的哈希碰撞
            unique_str = f"{i}_{text[:50]}"
            hash_id = hashlib.md5(unique_str.encode('utf-8')).hexdigest()
            ids.append(hash_id)
        self.collection.add(
            documents=datas,
            embeddings=embs,
            ids=ids,
            metadatas=[{"source_question": inst} for inst in datas]
        )
        print(f"成功导入 {len(ids)} 条数据")

    def search(self, query, model, ct, n_results=3):
        query_emb = self.get_embedding([query], model, ct)
        res = self.collection.query(
            query_embeddings=query_emb,
            n_results=n_results,
            include=["documents", "metadatas", "distances"]  # 获取更多信息
        )
        return res

    # 封装提示词模板
    def concat_prompt(self,prompt,query,INFO):
        tprompt = prompt
        tquery = query
        tINFO = INFO
        # clt = self.gettoenv()
        # model = self.getModel()
        prompt = tprompt.replace('__INFO__', '\n'.join(INFO['documents'][0])).replace('__QUERY__',query)
        return prompt

# 第三步 生成内容,创建一个聊天机器人进行问答内容的回答
# 答案生成器
class Rag_Bot:
    def __init__(self,prompt,client):
        self.prompt = prompt
        self.client = client

    def get_llm(self):
        messages = [{"role": "user", "content": self.prompt}]
        response = self.client.chat.completions.create(model='qwen3-max', messages=messages)
        # print(response)
        return response.choices[0].message.content

    def chat(self):
        return self.get_llm()

if __name__ == '__main__':
    # 定义提示词
    # 训练  奖惩机制
    # __INFO__  通过检索到的数据  进行替换
    # __QUERY__ 替换用户提的问题
    prompt_template = """
            你是一个问答机器人。
            你的任务是根据下述给定的已知信息回答用户问题。
            确保你的回复完全依据下述已知信息。不要编造答案。
            如果下述已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。    

            已知信息:
            __INFO__

            用户问：
            __QUERY__

            请用中文回答用户问题。
            """
    # 定义用户问题请求
    query = "财务管理权限划分"

    # 处理文档
    mreadstart = readPdf_split('财务管理文档.pdf')
    data = mreadstart.open_pdf()
    # print(data)


    # 文档内容向量化存入向量数据库中
    mlocadb = MylocahostDBbase('test')
    # 执行一次即可
    # mlocadb.add_documents(data)
    model = mlocadb.getModel()
    ct = mlocadb.gettoenv()
    # 通过问题获得向量数据库中的答案内容
    res = mlocadb.search(query, model, ct)
    # 获取新的提示词模板
    new_prompt_template = mlocadb.concat_prompt(prompt_template,query,res)
    # print(new_prompt_template)

    chat = Rag_Bot(new_prompt_template,ct)
    zz_res = chat.chat()
    print(zz_res)
