# 整数与浮点的特性
import sys

# 整数的特性
print(sys.getsizeof(0))     # 24 字节（空整数基础开销）
print(sys.getsizeof(1))     # 28 字节（小整数）
print(sys.getsizeof(2**30)) # 32 字节（需要2个digit）
print(sys.getsizeof(2**60)) # 36 字节（需要3个digit）
# 每增加约30位（2^30 ≈ 10亿），增加4字节
print(sys.getsizeof(2**90)) # 40 字节（需要4个digit）

# 浮点数的特性
print(sys.getsizeof(3.14))  # 24 字节（16字节对象头 + 8字节数值）


'''
    int 整型, 占⽤ 4 个字节空间, 总有 4 * 8 = 32 个⽐特位. 31个⽐特位可以存储数
据. 正数 2147483648 负值 -2147483647
 unsigned int, unsigned long ⽆符号类型, 只能存储正数, 不能存储负数. 4294967
296, 18446744073709551616
 long ⻓整型, 占⽤ 8 个字节空间, 最⼤值为 9223372036854775808
 float 单精度浮点型 4个字节, double 双精度浮点型 8 个字节
 
 1.整数的英⽂是 integer, 在计算机程序语⾔中⼀般⽤ int 表示. 整数⼤⼩必须在某⼀区间, 否则会有
溢位(overflow), 造成数据不正确. Python3已经将整数存储空间的⼤⼩限制拿掉了, 所有没有 long
了, 也就是说 int 可以是任意⼤⼩的数值
 2.浮点数的英⽂是 float, 既然整数⼤⼩没有限制, 浮点数⼤⼩当然也没有限制
'''

n = 2**31
print(f'{n = }')


# 字符串类型
'''
前缀组合	含义	示例
f''	格式化字符串	f"Hello {name}"
r''	原始字符串	r"C:\path"
b''	字节字符串	b'\x48\x65\x6c'
fr'' / rf''	原始格式化字符串	fr"C:\{folder}"
rb''	原始字节字符串	rb"\x48\x65"
u''	Unicode（Python 3中冗余）	u"text"    u'你好' 会将字符串以 Unicode 编码格式进行存储，常用于文本处理
'''

t0 = '你好啊'
print(f'{t0 = }',type(t0))

t1 = 'G:\图灵AI\其他资料'
print(t1,t1,type(t1))
print(fr'{t1 = }',type(t1))

t2 = r'G:\图灵AI\其他资料'
print(f'{t2 = }',type(t2))

t3 = 'hello ttt'
print('t3 =',t3,type(t3))
print(f'{b'{t3}' = }',type(b'{t3}'))

t4 = fr'cool ni jiw '
print(f'{t4 = }',type(t4))

t5 = u'你好啊'
print(f'{t5 = }',type(t5))
print(f'{b'{t5}' = }',type(b'{t5}'))





