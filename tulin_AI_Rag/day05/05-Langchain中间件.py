#!/usr/bin/env python
# -*- coding: UTF-8 -*-



from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
import os
from dotenv import load_dotenv
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

load_dotenv()


# 定义查询订单状态的函数
def query_order_status(order_id):
    if order_id == "1024":
        return "订单 1024 的状态是：已发货，预计送达时间是 3-5 个工作日。"
    else:
        return f"未找到订单 {order_id} 的信息，请检查订单号是否正确。"


# 定义退款政策说明函数
def company_refund_policy(company_name):
    print(company_name)
    if company_name == "tom":
        return "tom公司的退款政策是：在购买后7天内可以申请全额退款，需提供购买凭证。"
    else:
        print('输入有误')


# 查询年龄
def get_age(name):
    if name == "tom":
        print(name)
        return "我的年龄是56岁！"
    else:
        print('输入有误')


# 初始化工具
tools = [
    TavilySearch(max_results=1, tavily_api_key=os.getenv("TAVILY_API_KEY")),
    Tool(
        name="queryOrderStatus",
        func=query_order_status,
        description="根据订单ID查询订单状态",
        args={"order_id": "订单的ID"}
    ),
    Tool(
        name="companyRefundPolicy",
        func=company_refund_policy,
        description="查询某某公司退款政策详细内容",
        args={"company_name": "公司名称"}
    ),
    Tool(
        name="getAge",
        func=get_age,
        description="查询tom年龄大小",
        args={"name": "查询tom年龄大小"}
    ),
]

# 选择将驱动代理的LLM
llm = ChatOpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"),
                 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                 model='qwen-plus')


agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="你是一个客服助手，使用工具回答问题。",
    # 使用中间件机制
    middleware=[
        # 指定需要人工决策的工具
        HumanInTheLoopMiddleware(
            interrupt_on={
                'tavily_search': {'allowed_decisions': ["approve", "reject"]},
                'queryOrderStatus': {'allowed_decisions': ["approve", "reject"]},
                'companyRefundPolicy': {'allowed_decisions': ["approve", "reject"]},
                'getAge': {'allowed_decisions': ["approve", "reject"]},
            }
        )
    ],
    # 对话历史、状态等都会保存在内存中
    # 让 agent 代理具备“记住对话历史 + 支持中断后继续”的能力
    checkpointer=InMemorySaver(),
)

# 定义一些测试询问
queries = [
    "请问订单1024的状态是什么？",
    "请问tom公司退款政策是什么？",
    "2024年谁胜出了美国总统的选举"
]

# 为当前会话设置唯一的 thread_id
# 同一个 thread_id 会保留完整的对话状态和中断历史
# 可以理解为一个ai工具运行一个会话
config = {"configurable": {"thread_id": "some_other_id_123"}}

# 运行代理并输出结果
for que in queries:
    print('客户提问：' + que)
    inputs = {"messages": [{"role": "user", "content": que}]}
    # # 执行代理，直到遇到中断或完成
    result = agent.invoke(inputs, config=config)
    # print(result)
    """
        result = {
            # ... 可能有一些已经执行完的部分，比如 messages 历史
            'messages': [...],           # 到目前为止的消息历史

            '__interrupt__': [           # 这是一个列表，通常长度为1（或多个，如果同时有多个待审工具）
                Interrupt(
                    value={
                        'action_requests': [          # 等待审核的工具调用列表
                            {
                                'name': 'tavily_search',  # 工具名
                                'args': {...},            # 工具要接收的参数（JSON）
                                'description': '...',     # 可选的描述
                                ...
                            },
                            # 如果有多个待审工具，这里可能有多个
                        ],
                        'review_configs': [...]       # 每个工具允许的决策类型（approve/reject 等）
                    },
                    # 其他内部字段...
                )
            ],
            # ... 其他字段
        }

        """
    tool_name = result['__interrupt__'][0].value['action_requests'][0]['name']
    # print(tool_name)
    app_or_reject = input("请确认调用{}是否同意(approve or reject)：".format(tool_name))
    # print(app_or_reject)
    # 构造恢复指令
    res = agent.invoke(
        Command(resume={'decisions': [{'type': app_or_reject}]}),
        config=config
    )
    print(res['messages'][-1].content)
    # for i in res['messages']:
    #     print('*' * 20)
    #     print(i)



# 4个左右作业   鲁棒性

