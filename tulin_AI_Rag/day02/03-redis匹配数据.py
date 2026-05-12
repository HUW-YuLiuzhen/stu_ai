#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import json
import redis

'''
- Redis，英文全称是[Remote Dictionary Server](https://zhida.zhihu.com/search?content_id=235651583&content_type=Article&match_order=1&q=Remote+Dictionary+Server&zhida_source=entity)（远程字典服务），是一个开源的使用[ANSI C](https://zhida.zhihu.com/search?content_id=235651583&content_type=Article&match_order=1&q=ANSI+C&zhida_source=entity)语言编写、支持网络、可基于内存亦可持久化的日志型、Key-Value数据库，并提供多种语言的API。
- 与MySQL数据库不同的是，Redis的数据是存在内存中的。它的读写速度非常快，每秒可以处理超过10万次读写操作。因此redis被广泛应用于缓存，另外，Redis也经常用来做分布式锁。除此之外，Redis支持事务、持久化、[LUA 脚本](https://zhida.zhihu.com/search?content_id=235651583&content_type=Article&match_order=1&q=LUA+%E8%84%9A%E6%9C%AC&zhida_source=entity)、LRU 驱动事件、多种集群方案。

- 使用教程: https://www.cnblogs.com/ahmao/p/13746094.html 
- 下载地址: https://github.com/tporadowski/redis/releases
'''


# 创建 Redis 连接
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)


# 从JSON文件中读取数据
def read_data():
    with open('train_zh.json', 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]

    # print(data[0:100])
    instructions = [entry['instruction'] for entry in data[0:10]]
    outputs = [entry['output'] for entry in data[0:10]]
    return instructions, outputs


# 将读取出来的数据存入Redis中
def set_redis_documents(instructions, outputs):
    for instruction, output in zip(instructions, outputs):
        r.set(instruction, output)


# 在Redis中根据关键词进行模糊搜索
def search_instructions(instruction_key, top_n=3):
    keys = r.keys(pattern='*' + instruction_key + '*')
    data = []
    for key in keys:
        data.append(r.get(key))
    return data[:top_n]


# 先从文件中读取数据
instructions, outputs = read_data()
# 在把数据存入到Redis中
set_redis_documents(instructions, outputs)
# 在Redis中进行检索
data = search_instructions('怀孕')
print(data)
