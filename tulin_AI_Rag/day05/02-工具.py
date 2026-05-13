#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# from langchain_tavily import TavilySearch
# from dotenv import load_dotenv
# import os
#
# load_dotenv()
#
#
# tool = TavilySearch(tavily_api_key=os.getenv("TAVILY_API_KEY"))
# print(tool)
# print("*" * 20)
# print(tool.name)
# print("*" * 20)
# print(tool.description)
# print("*" * 20)
# print(tool.args)
#
# aa = tool.invoke({'query': '大模型是什么'})
# print(aa)


# 自定义工具
from langchain.tools import tool

@tool
def add_number(a: int, b: int) -> int:
    """add two numbers."""
    return a + b

print(add_number.name)
print(add_number.description)
print(add_number.args)



