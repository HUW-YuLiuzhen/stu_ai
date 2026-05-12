import re


# text = "自然语言处理（NLP），作为计算机科学、人工智能与语言学的交融之地，致力于赋予计算机解析和处理人类语言的能力。在这个领域，机器学习发挥着至关重要的作用。利用多样的算法，机器得以分析、领会乃至创造我们所理解的语言。从机器翻译到情感分析，从自动摘要到实体识别，NLP的应用已遍布各个领域。随着深度学习技术的飞速进步，NLP的精确度与效能均实现了巨大飞跃。如今，部分尖端的NLP系统甚至能够处理复杂的语言理解任务，如问答系统、语音识别和对话系统等。NLP的研究推进不仅优化了人机交流，也对提升机器的自主性和智能水平起到了关键作用。"

# 第一种 正则匹配拆分
# result_1 = re.split(r'(。|？|！|\..\..)', text)
# print(result_1)
# chunks = []
# for sentence, punctuation in zip(result_1[::2], result_1[1::2]):
#     # print(f'{sentence}')
#     # print(f'{punctuation= }')
#     chunks.append(sentence + (punctuation if punctuation else ''))
#
# # print(chunks)
# for i, chunk in enumerate(chunks):
#     print(f"块 {i + 1}: {len(chunk)}: {chunk}")



# 第二种 按照固定字符数进行切割
# def get_str_split(text,count):
#     chunks_1 = []
#     for i in range(0,len(text),count):
#         chunks_1.append(text[i:i+count])
#     return chunks_1
#
# t_chunks = get_str_split(text,50)
# print(t_chunks)
# for i,t in enumerate(t_chunks):
#     print(f'块 {i+1} ： {len(t)} : {t}')

# 第三种  按固定字符数 结合overlapping window 进行字符串重叠的方式截取
# def get_str_split2(text,size,stride):
#     chunks_1 = []
#     # print(len(text))
#     for i in range(0,len(text),stride):   # 从0开始取值，没50个为一组
#         # print(f'{i} : {i+size}')
#         chunks_1.append(text[i:i+size]+"\n")
#     return chunks_1
#
# t_chunks2 = get_str_split2(text,100,50)  #按照100个字符切割为一段，其中50个字符是重复的
# print(t_chunks2)
# for i,t2 in enumerate(t_chunks2):
#     print(f'块 {i} : {len(t2)} : {t2}')


# 第四种 递归方法
# 模块下载 pip install langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter

'''
    RecursiveCharacterTextSplitter 是一个用于将文本分割成较小块的工具。
    它特别适用于需要递归地按字符拆分文本的场景，例如处理超长文档或嵌套结构的文本
    chunk_size = 分割长度
    chunk_overlap = 重叠长度
    length_function = 固定写法（用于定义如何计算每个文本片段的长度）
'''

text = "自然语言处理（NLP），作为 计算机科学、人工 智能与语言学 的交融之地，致力于赋予计算机解析和处理人类语言的能力。在这个领域，机器学习发挥着至关重要的作用。利用多样的算法，机器得以分析、领\n会乃至创造我们所理解的语言。从机器翻译到情感分析，从自动摘要到实体识别，NLP的应用已遍布各个领域。随着深度学习技术的飞速进步，NLP的精确度与效能均实现了巨大飞跃。如今，部分尖端的NLP系统甚至能够处理复杂的语言理解任务，如问答系统、语音识别和对话系统等。NLP的研究推进不仅优化了人机交流，也对提升机器的自主性和智能水平起到了关键作用。"


splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=25,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]  # 根据特殊字符循环拆分
)
'''
分割器按照 separators 列表的顺序依次尝试分割：

第1轮：尝试用 \n\n(双换行)分割
如果某个块仍 >50字符，进入下一轮

第2轮：尝试用 \n(单换行)分割
如果某个块仍 >50字符，进入下一轮

第3轮：尝试用 (空格)分割
如果某个块仍 >50字符，进入下一轮

第4轮：用 ""(空字符串，即按字符)强制分割
确保所有块都不超过 chunk_size
'''


split_text = splitter.split_text(text)
print(split_text)
for i,t in enumerate(split_text):
    print(f'{i} : {len(t)} : {t}')







