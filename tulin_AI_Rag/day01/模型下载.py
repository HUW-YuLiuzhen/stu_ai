#  第一种  这个是魔塔的模型离线下载方式
# 安装 ModelScope
# pip install modelscope

# from modelscope import snapshot_download


# model_dir = snapshot_download('iic/nlp_gte_sentence-embedding_chinese-small',cache_dir=r"G:\locahost_llm\nlp_gte_sentence-embedding_chinese-small")



# 第二种 HuggingFace 模型下载   待后续再研究吧
from transformers import AutoModel, AutoTokenizer

model_name = "jinaai/jina-embeddings-v5-text-small"
cache_dir = r"G:\locahost_llm\jinaaijina-embeddings-v5-text-small"

model = AutoModel.from_pretrained(model_name, cache_dir=cache_dir)
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)