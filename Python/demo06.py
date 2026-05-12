"""
    分支结构：
        单分支
        双分支
        多分支
        match匹配语句
"""

# 单分支
# tz,ll,mj,zh =eval(input("请初始化张三的体质,力量,敏捷,智力属性 \n\f"))
#
# if  tz >= ll and tz >= mj and tz >= zh:
#     print("您是一位长跑选手，体质为："+f'{tz= }')
#
# if ll >= tz and ll >= mj and ll >= zh:
#     print("您是一位力量选手，力量为: "+f'{ll= }')

# 双分支
# t = eval(input("请输入一个数字： "))
# #
# # if t%2 == 0:
# #     print("您输入的数字为 ："+ f'{t}' + " 是一个偶数")
# # else:
# #     print("您输入的数字为 ："+ f'{t}' + " 是一个奇数")
#
# # 双分支简化版本
# # n(判断条件成立，取n) if  判断条件  else  x(判断条件不成立取x)
# str1 = "您输入的数字为 ："+ f'{t}' + " 是一个偶数" if t%2 == 0 else "您输入的数字为 ："+ f'{t}' + " 是一个奇数"
# print(str1)
# 多分支
# 根据输入整形数据判断属于什么级别冒险者
mlevle = eval(input("请输入属性值，以便做初次等级评价 ："))

if mlevle >= 100:
    print("恭喜你成为SSS级冒险者")
elif mlevle >= 95:
    print("恭喜你成为SS级冒险者")
elif mlevle >= 90:
    print("恭喜你成为S级冒险者")
elif mlevle >= 80:
    print("恭喜你成为A级冒险者")
elif mlevle >= 70:
    print("恭喜你成为B级冒险者")
elif mlevle >= 60:
    print("恭喜你成为C级冒险者")
elif mlevle >= 50:
    print("恭喜你成为D级冒险者")
else:
    print("恭喜你成为不入流冒险者")

# match匹配语句
match mlevle:
    case _ if mlevle>=100:
        print("恭喜你成为SSS级冒险者")
    case _ if mlevle >= 95:
        print("恭喜你成为SS级冒险者")
    case _ if mlevle >= 90:
        print("恭喜你成为S级冒险者")
    case _ if mlevle >= 80:
        print("恭喜你成为A级冒险者")
    case _ if mlevle >= 70:
        print("恭喜你成为B级冒险者")
    case _ if mlevle >= 60:
        print("恭喜你成为C级冒险者")
    case _ if mlevle >= 50:
        print("恭喜你成为D级冒险者")
    case _:  # 兜底写法 相当于  else
        print("恭喜你成为不入流冒险者")

    
