"""
    函数定义
    定义的写法如下 def + 函数名字(传参：类型,.....) -> 返回值类型：
     返回值类型 void, int, float, double, list, dic
"""
# 第一种默认写法
def greeting(name : str,age:int):
    print("Hello %s!" % name + "恭喜妳年满：" + str(age)+"岁")

greeting("张三",11)

# 第二种 固定返回类型的写法 ，若不写返回值 默认返回None
def returnString(name : str,age:int)->str:
    mName = name.title()
    mAge = age
    return f'{mName}'+"你是一个年满"+f'{mAge}'+"岁的男子汉了"

aString = returnString("王五",10)
print(aString)

# 回传多个返回参数的写法
def math_operation(a:int,b:int)->int:
    mjf = a+b #加法
    mjjf = a-b #剪法
    mcf = a*b #乘法
    mccf = a//b  #除法
    return mjf,mjjf,mcf,mccf

result = math_operation(10,20)
print(f'{result = }',id(result),type(result))

# 传入参数不确定个数和格式的写法
def math_operation(*args)->int:
    # args 本质是一个元组类型数据
    res = 0
    for arg in args:
        res += arg
    return res

result1 = math_operation(1,2,3,4,5,6,7,8,9,10)
print(result1)

# 定义关键字参数 函数  **kwargs  全称 keyword arguments 关键字参数, 本质是⼀个字典类型
def return_student(name : str,**kwargs) -> dict:
    mName = name.title()
    mAge = kwargs.get('age')
    mMath = kwargs.get('math')
    mEnglish = kwargs.get('english')
    mChinese = kwargs.get('chinese')
    maxsorce = mMath + mEnglish + mChinese
    return "名字："+f'{mName}'+"年龄："+f'{mAge}'+"总成绩："+f'{maxsorce}'

result2 = return_student("王五",age=19,math=89,english=68,chinese=80)
print(result2)

# 匿名函数
# 匿名函数最⼤特⾊是可以有许多的参数, 但是只能有⼀个程序表达式, 然后可以将执⾏结果回传
# 匿名函数 lambda 的语法
# 正常写法
def query(x):
    return x*x

print(query(4))

# lambda 写法
l = lambda x: x*x
print(l(4))
print((lambda x: x*x)(4))

# 过滤函数 filter(func, iterable) 过滤函数
# 正常写法
zglist = [i for i in range(1,10,1)]
print(zglist)

# 通过匿名写法 + filter 过滤函数进行过滤 获取到 能被2整除的 10以内的数据
# r = filter(lambda x: x % 2 == 0, zglist)
# print(r)

t = list(filter(lambda x: x % 2 == 0, zglist))
print(t)

# pass 让当前函数通过语法检测
# def greeting(name, age):
# pass # 让语法检测先通过


