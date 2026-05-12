#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# OpenAI 兼容
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# 创建一个连接
client = OpenAI(api_key=os.getenv('bail_api_key'), base_url=os.getenv('bail_base_url'))
# api_key = os.getenv('bail_api_key')
# base_url = os.getenv('bail_base_url')
# print(f'{api_key = } :  {base_url = }')

# 定义一个文本内容向量化的方法
def get_embedding(text):
    data = client.embeddings.create(input=text, model='text-embedding-v4')
    # print(data)
    return [i.embedding for i in data.data]


test_query = ['我爱你', '你好']

vec = get_embedding(test_query)
print(vec)
print(len(vec[0]))  # 千问v1模型 1536维   v3 1024
# 构建知识库的时候  用的v1 模型     查询 能不能用v3










