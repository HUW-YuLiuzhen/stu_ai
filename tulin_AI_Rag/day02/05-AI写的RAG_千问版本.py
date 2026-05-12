import os
import uuid
from typing import List, Dict, Any
from pypdf import PdfReader
import chromadb
from chromadb import Documents, Embeddings
# 引入 EmbeddingFunction 类型提示（虽然不强制继承，但有助于开发）
from chromadb.api.types import EmbeddingFunction
from dashscope import TextEmbedding
from dotenv import load_dotenv
import dashscope

# --- 1. 配置区 ---
load_dotenv()
DASHSCOPE_API_KEY = os.getenv('bail_api_key')
if not DASHSCOPE_API_KEY:
    DASHSCOPE_API_KEY = os.getenv('bail_api_key')

# 显式设置 API Key 到环境变量，防止 dashscope 库找不到 key
if DASHSCOPE_API_KEY:
    os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY

PDF_PATH = "财务管理文档.pdf"


# --- 2. 修复版 Embedding 类 (适配新版 ChromaDB) ---
class BailianEmbeddingFunction:
    """
    自定义 Embedding 类，必须包含 __call__ 方法、embed_query 方法和 name 属性。
    """

    def __init__(self):
        # 定义模型名称，用于 ChromaDB 内部标识
        self._name = "text-embedding-v2"
        # 关键修复1: 在初始化时，将获取到的 API Key 显式赋值给 dashscope 库
        if DASHSCOPE_API_KEY:
            dashscope.api_key = DASHSCOPE_API_KEY

    def name(self) -> str:
        # 提供 name() 方法
        return self._name

    def __call__(self, input: Documents) -> Embeddings:
        """
        批量处理：接收文本列表，返回向量列表
        用于 add_documents 时的批量入库
        """
        try:
            # 调用 DashScope API
            response = TextEmbedding.call(
                model=TextEmbedding.Models.text_embedding_v2,
                input=input
            )

            if response.status_code == 200:
                # 提取向量结果
                return [item['embedding'] for item in response.output['embeddings']]
            else:
                print(f"❌ Embedding API 错误: {response.code} - {response.message}")
                # 返回零向量占位
                return [[0.0] * 1536] * len(input)

        except Exception as e:
            print(f"❌ 调用 Embedding 发生异常: {e}")
            return [[0.0] * 1536] * len(input)

    # ⚠️ 新增方法：专门处理单条查询
    def embed_query(self, input: str) -> List[float]:
        """
        单条处理：接收单个字符串，返回单个向量
        用于 search 时的用户提问
        """
        try:
            response = TextEmbedding.call(
                model=TextEmbedding.Models.text_embedding_v2,
                input=[input]  # 注意：API 需要列表，所以包一层
            )

            if response.status_code == 200:
                # 关键修复2: 返回一个二维列表，即包含单个向量的列表
                return [response.output['embeddings'][0]['embedding']]
            else:
                print(f"❌ 查询 Embedding API 错误: {response.code} - {response.message}")
                # 关键修复2: 返回一个二维列表
                return [[0.0] * 1536]

        except Exception as e:
            print(f"❌ 查询 Embedding 发生异常: {e}")
            # 关键修复2: 返回一个二维列表
            return [[0.0] * 1536]

# --- 3. PDF 解析与智能切分 ---
def load_and_split_pdf(pdf_path: str, chunk_size: int = 500) -> List[Dict[str, Any]]:
    reader = PdfReader(pdf_path)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    # 智能切分逻辑
    paragraphs = full_text.replace('\n', '').replace(' ', '').split('。')

    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + "。"
        else:
            if current_chunk:
                chunks.append({
                    "id": str(uuid.uuid4()),
                    "content": current_chunk.strip(),
                    "metadata": {"source": pdf_path}
                })
            current_chunk = para + "。"

    if current_chunk:
        chunks.append({
            "id": str(uuid.uuid4()),
            "content": current_chunk.strip(),
            "metadata": {"source": pdf_path}
        })

    print(f"✅ 文档解析完成，共切分为 {len(chunks)} 个片段。")
    return chunks


# --- 4. RAG 知识库类 ---
class PureRAGDatabase:
    def __init__(self, db_path: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)

        # 实例化自定义 Embedding 类
        self.embedding_func = BailianEmbeddingFunction()

        # 创建集合，传入实例化的对象
        self.collection = self.client.get_or_create_collection(
            name="financial_policy",
            embedding_function=self.embedding_func,  # 传入对象而非函数
            metadata={"hnsw:space": "cosine"}
        )
        print("🚀 RAG 知识库初始化完成。")

    def add_documents(self, documents: List[Dict[str, Any]]):
        if not documents:
            return

        ids = [doc["id"] for doc in documents]
        texts = [doc["content"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]

        self.collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
        print(f"💾 成功将 {len(documents)} 个片段存入向量数据库。")

    def search(self, query: str, n_results: int = 3) -> Dict[str, Any]:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        print(f"\n🔍 检索问题: {query}")
        print("--- 检索到的相关片段 ---")

        if not results['documents'][0]:
            print("未找到相关结果。")
            return results

        for i, (doc, meta, dist) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0] if 'distances' in results else []
        )):
            print(f"\n【匹配度 {i + 1} (距离: {dist:.4f}) | 来源: {meta['source']}】")
            print(doc.strip())

        return results


# --- 5. 主程序 ---
def main():
    rag_db = PureRAGDatabase()

    if rag_db.collection.count() == 0:
        print("📂 数据库为空，正在加载文档...")
        if not os.path.exists(PDF_PATH):
            print(f"❌ 错误: 找不到文件 {PDF_PATH}")
            return

        docs = load_and_split_pdf(PDF_PATH)
        rag_db.add_documents(docs)
    else:
        print(f"📂 数据库已存在，当前共有 {rag_db.collection.count()} 条记录。")

    rag_db.search("佛山电器照明的财务审批权限是如何规定的？")


if __name__ == "__main__":
    main()