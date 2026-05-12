# 变量赋值后，相同赋值变量，其内存地址是一致的

#整形案例
number1 = 1000
number2 = 1000

print(f'{type(number1) = }， {type(number2) = }')
print(f'{id(number1) = }, {id(number2) = } ')

# 浮点案例
num1 = 10.5
num2 = 10.5
print(f'{type(num1) = },{type(num2) = }')
print(f'{id(num1) = }, {id(num2) = }')

# 字符串案例
num3 = "hello"
num4 = 'hello'
print(f'{type(num3) = },{type(num4) = }')
print(f'{id(num3) = }, {id(num4) = }')


# 除法案例
num5 = 10 / 3  # 浮点除
num6 = 10 // 3 # 整除
num7 = 10 % 3 # 余数
print(f'{type(num5) = },{type(num6) = }，{type(num7) = }')
print(f'{id(num5) = }, {id(num6) = }，{id(num7) = }')
print(f'{num5 = }, {num6 = }, {num7 = }')

# 内置函数求余
print(f'{divmod(10,3) = }')

# 二进制
print(f'{2**0 = }')
print(f'{2**1 = }')
print(f'{2**2 = }')
print(f'{2**3 = }')
print(f'{2**4 = }')
print(f'{2**5 = }')
print(f'{2**6 = }')
print(f'{2**7 = }')

# 10进制
print(f'{10**0 =}')
print(f'{10**1 =}')
print(f'{10**2 =}')
print(f'{10**3 =}')
print(f'{10**4 =}')
print(f'{10**5 =}')
print(f'{10**6 =}')

# 每天进步0.1%的复利计算公式，要求计算一年的复利结果
print(f'{1000*(1+0.001)**365 = }')
print(f'{(1+0.001)**365:.2f} ')
print(f'{(1+0.001)**365 = :.2f} ')

# 计算每天退步0.1%的复利计算公式，要求计算一年的复利结果
print(f'{1000*(1-0.001)**365 = }')
print(f'{(1-0.001)**365:.2f} ')
print(f'{(1-0.001)**365 = :.2f} ')
