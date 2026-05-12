# langchain_huggingface 加载huggingface模型
from langchain_huggingface import HuggingFaceEmbeddings

# 创建嵌入模型
model_name = r"G:\locahost_llm\nlp_gte_sentence-embedding_chinese-small\iic\nlp_gte_sentence-embedding_chinese-small"

# 生成的嵌入向量将被标准化, 有助于向量比较
encode_kwargs = {'normalize_embeddings': True}

embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    encode_kwargs=encode_kwargs
)
text = "大模型"
query_result = embeddings.embed_query(text)
print(query_result)