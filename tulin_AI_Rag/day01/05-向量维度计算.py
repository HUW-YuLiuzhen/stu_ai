import numpy as np
from numpy import dot
from numpy.linalg import norm
from openai import OpenAI
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer



#  第一步创建client连接

# 第二步定义计算cos余弦的方法 和 计算欧氏距离的方法

# 第三步 定义一个向量转换的方法

# 第四步 定义一个 main方法进行数据调用

def gettoenv():
    load_dotenv()
    client = OpenAI(api_key=os.getenv('bail_api_key'), base_url=os.getenv('bail_base_url'))
    return client

# 定义余弦计算方法
def get_codsin(**kwargs):
    # 计算点积
    a = kwargs.get('a')
    b = kwargs.get('b')
    fz = dot(a, b)
    # 计算分母
    fm = norm(a)*norm(b)
    return fz/fm

# 定义欧氏距离计算方法
def get_osju(**kwargs):
    a = kwargs.get('a')
    b = kwargs.get('b')

    os_a = np.asarray(a)
    os_b = np.asarray(b)

    os_c = norm(os_a-os_b)
    return os_c


# 定义一个embedding的计算方法 -在线版本
def get_embedding(text,model,ct):
    data = ct.embeddings.create(input=text, model=model)
    # print(data)
    return [i.embedding for i in data.data]
# 定义一个离线版本的embedding计算方法
def get_lx_embedding(text,model_path):
    sentences = text
    model = SentenceTransformer(model_path)
    embeddings = model.encode(sentences, normalize_embeddings=True)
    # print(embeddings)
    return embeddings


if __name__ == '__main__':
    a = (1,2,3)
    b = (4,5,6)

    # 余弦值
    yx_math = get_codsin(a=a,b=b)
    print(f'余弦计算 : {yx_math}')

    # 欧氏距离
    os_math = get_osju(a=a,b=b)
    print(f'欧氏距离计算 ： {os_math}')

    # 定义一个问题 和 答案然后调用embedding模型
    query = "我国开展舱外辐射生物学暴露实验"
    docments = ("联合国就苏丹达尔富尔地区大规模暴力事件发出警告",
    "土耳其、芬兰、瑞典与北约代表将继续就瑞典“入约”问题进行谈判",
    "日本岐阜市陆上自卫队射击场内发生枪击事件 3人受伤",
    "国家游泳中心（水立方）：恢复游泳、嬉水乐园等水上项目运营",
    "我国首次在空间站开展舱外辐射生物学暴露实验")
    # 定义需要使用的模型
    model = "text-embedding-v4"

    # 初始化一个模型连接器
    client = gettoenv()
    # 获得 问题的向量值
    data_query = get_embedding(query,model,client)[0]
    # print(f'{data_query = } : {len(data_query)} : {type(data_query)}')
    # 获得 答案的向量值
    date_docments = get_embedding(docments,model,client)

    # print(f'{date_docments = } : {len(date_docments)} : {type(date_docments)}')
    print("\n")
    print("线上版本的embedding计算————————start")
    # 计算问题的余弦值
    for i,d in enumerate(date_docments):
        # 余弦相似度，越大越相似
        data_cos = get_codsin(a=data_query,b=d)
        print(f'编号:{i + 1} , 余弦相似度: {data_cos:}')
        print(f'编号:{i + 1} , 余弦相似度: {data_cos:.4f}')  # .4f 保留四位小数
        # 欧氏距离是越小越准
        data_os = get_osju(a=data_query,b=d)
        print(f'编号:{i + 1} , 欧氏距离: {data_os:}')
        print(f'编号:{i + 1} , 欧氏距离: {data_os:.4f}')  # .4f 保留四位小数

    print("线上版本的embedding计算————————end\n\n\t")

    # 玩一下离线模型
    # 定义本地模型地址
    print("离线版本的embedding计算————————start")
    model_path = r"G:\locahost_llm\nlp_gte_sentence-embedding_chinese-small\iic\nlp_gte_sentence-embedding_chinese-small"
    data_query_lx = get_lx_embedding(query,model_path)
    data_query_os_lx = get_lx_embedding(docments,model_path)

    for i,d in enumerate(data_query_os_lx):
        data_cos_lx = get_codsin(a=data_query_lx,b=d)
        print(f'编号:{i + 1} , 余弦相似度: {data_cos_lx:}')
        print(f'编号:{i + 1} , 余弦相似度: {data_cos_lx:.4f}')  # .4f 保留四位小数
        data_os_lx = get_osju(a=data_query_lx,b=d)
        print(f'编号:{i + 1} , 欧氏距离: {data_os_lx:}')
        print(f'编号:{i + 1} , 欧氏距离: {data_os_lx:.4f}')  # .4f 保留四位小数

    print("离线版本的embedding计算————————end\n\n\t")