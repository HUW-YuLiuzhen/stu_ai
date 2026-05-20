from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()
LLM = ChatOpenAI(api_key=os.getenv("bail_api_key"),
                      base_url=os.getenv("bail_base_url"),model="qwen3.6-plus")

Embedding_path = os.getenv("Embedding_path")
# Embedding_path = r'G:\locahost_llm\nlp_gte_sentence-embedding_chinese-small\iic\nlp_gte_sentence-embedding_chinese-small'
Embedding_model = HuggingFaceEmbeddings(model_name=Embedding_path)