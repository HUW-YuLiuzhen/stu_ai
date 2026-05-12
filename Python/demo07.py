"""
循环结构
    for循环
    while循环
"""


# # for 循环
# # 第一题：循环输出10次我爱爸妈
# for i in range(10):
#     print(f'{i}' + "我爱爸妈")
#
# # 第二题： 循环遍历一个list序列
# alist = list(range(15))
# for i in alist:
#     print(f'{i}' + "我爱我爱的人")
#
# blist = [1,2,3,4,5,8,10]
# for i in blist:
#     print(f'{i}' + "我爱爱我的人")
#
# # 第三题: 循环字符串
# aStr ="hello  python3"
# for e in aStr:
#     print(e)
#
# # 第四题：生成10个0的列表对象
# clist = [0]*10
# print(f'{clist = }',id(clist),type(clist))
# for i in clist:
#     print(i)

# 第五题：取1-100 之间的奇数
# for i in range(1,101,2):
#     print(i)
# 将1-100的奇数放到列表中去
dlist = [i for i in range(1,101,2)]
print(dlist)

print("\n")
# 列出100以内的勾股函数
# for a in range(1,101,1):
#     for b in range(a,101,1):
#         for c in range(b,101,1):
#             if a**2 + b**2 == c**2:
#                 print(a,b,c)

# 将100以内的 勾股函数存入列表中
elist = [(a,b,c) for a in range(1,101,1) for b in range(a,101,1) for c in range(b,101,1) if a**2 + b**2 == c**2]
print(elist)


# while 循环
# 作业1：有⼀筐鸡蛋, ⾄少有两个, 两个两个数, 多⼀个, 三个三个数, 多⼀个, 四个四个数, 还是多⼀
# 个, 请问, ⾄少有⼏个?

#
count = eval(input("请输入数字: "))
while True:
    if count % 2 == 1 and count % 3 == 1 and count % 4 == 1 and count >= 2:
        print(f'{count = }')
        break
    count += 1

# 哨兵值
avlog = True
while avlog:
    inputvalue = input("请输入内容：")
    if inputvalue == "TC":
        avlog = False
    print(inputvalue)
