#  第一种  这个是魔塔的模型离线下载方式
# 安装 ModelScope
# pip install modelscope

# from modelscope import snapshot_download
#
#
# # model_dir = snapshot_download('xiaowangge/qwen3-embedding-0.6b')
# model_dir = snapshot_download('iicnlp_gte_sentence-embedding_chinese-small',cache_dir="G:\locahost_llm")

# from BCEmbedding import EmbeddingModel
# from sentence_transformers import SentenceTransformer
#
#
# sentences = ['我是一个水哥', '我是一个帅哥']
#
# # model = EmbeddingModel(model_name_or_path=r"G:\locahost_llm\gpustack\bce-embedding-base_v1")
# # model_path = r"D:\LLM\Local_model\BAAI\bge-large-zh-v1___5"
# model = SentenceTransformer(r"G:\locahost_llm\gpustack\bce-embedding-base_v1-GGUF")
#
# embeddings = model.encode(sentences)
#
# print(f'{embeddings} : {len(embeddings)}')



from sentence_transformers import SentenceTransformer

# list of sentences
sentences = ['我是你哥', '你是我弟弟']

# init embedding model
model = SentenceTransformer(r"G:\locahost_llm\nlp_gte_sentence-embedding_chinese-small\iic\nlp_gte_sentence-embedding_chinese-small")
# model = SentenceTransformer(r"G:\locahost_llm\bce-embedding-base_v1-GGUF\gpustack\bce-embedding-base_v1-GGUF")

# extract embeddings
embeddings = model.encode(sentences, normalize_embeddings=True)
print(f'{embeddings} : {len(embeddings)} : {embeddings.shape} ')






