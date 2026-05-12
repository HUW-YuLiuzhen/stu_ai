# 列表
# 1.定义一个列表对象
alist = []
print(f'{alist = }',type(alist),'-'*10,id(alist))

blist = list()
print(f'{blist = }',type(blist),'-'*10,id(blist))


# 2.CURD 增删改差操作
# 增  在往列表对象中增加元素的时候，内存空间是不会变化的  append(1)
clist = list()
clist.append(3)
print(f'{clist = }',type(clist),'-'*10,id(clist))
clist.append(2)
print(f'{clist = }',type(clist),'-'*10,id(clist))
clist.append(1)
print(f'{clist = }',type(clist),'-'*10,id(clist))

# 插入  insert(5,4)
clist.insert(5,4)
print(f'{clist = }',type(clist),'-'*10,id(clist))
clist.insert(4,7)
print(f'{clist = }',type(clist),'-'*10,id(clist))

# 弹出 默认弹出最后一个元素  下标都是从0开始到  pop()
element = clist.pop()
print(clist,element,type(clist),'-'*10,id(clist))

# 指定弹出元素  下标都是从0开始到  pop(3)
element1 = clist.pop(3)
print(clist,element1,type(clist),'-'*10,id(clist))

# 指定删除 ,指定删除具体元素  remove(3)
clist.remove(3)
print(f'{clist = }',type(clist),'-'*10,id(clist))

# 修改  clist[1] = 555
clist[1] = 555
print(f'{clist = }',type(clist),'-'*10,id(clist))


# 列表切片  切⽚的语法 (容器类型 / 序列类型)[start:end:step]  下标 : start=0, stop=10 (不包含) step = 1
alist1 = [1,2,3,4,5,6,7,8,9]
print(f'{alist1 = }',type(alist1),'-'*10,id(alist1))
blist1 = alist1[2:12:2]
print(f'{blist1 = }',type(blist1),'-'*10,id(blist1))

str1 = 'hello  word'
print(f'{str1 = }',type(str1),'-'*10,id(str1))
substr = str1[:7:]
print(f'{substr = }',type(substr),'-'*10,id(substr))


# 列表   sort()  排序  和 sorted()  的区别
alist2 = list(range(10))
print(f'{alist2 = }',type(alist2),'-'*10,id(alist2))

# 存取有序
blist2 = [2,3,4,9,8,7,6,1,5,11,10]
print(f'{blist2 = }',type(blist2),'-'*10,id(blist2))

# 升序  sort()
blist2.sort()
print('升序',f'{blist2 = }',type(blist2),'-'*10,id(blist2))

# 降序 sort(reverse=True)
blist2.sort(reverse=True)
print('降序',f'{blist2 = }',type(blist2),'-'*10,id(blist2))
# 反转顺序 reverse()
blist3 = [2,3,4,9,8,7,6,1,5,11,10]
print(f'{blist3 = }',type(blist3),'-'*10,id(blist3))
blist3.reverse()
print(f'{blist3 = }',type(blist3),'-'*10,id(blist3))

# 内置函数 sorted() 不是在原列表上进⾏排序的, ⽽是复制了⼀个新排列再实现排序. 所以操作  完毕后⼀定要接收返回的结果
alist4 = list([2,3,4,9,8,7,6,1,5,11,10])
print(f'{alist4 = }',type(alist4),'-'*10,id(alist4))
# 降序  sorted(alist4, reverse=True)
blist4 =  sorted(alist4, reverse=True)
print(f'{blist4 = }',type(blist4),'-'*10,id(blist4))
# 升序  sorted(alist4)
clist4 = sorted(alist4)
print(f'{clist4 = }',type(clist4),'-'*10,id(clist4))


# 元组 tuple()  一个定义后不可变的序列
tuple1 = [2,3,4,9,8,7,6,1,5,11,10]
print(f'{tuple1 = }',type(tuple1),'-'*10,id(tuple1))
tuple1[0] = 100
print(f'{tuple1 = }',type(tuple1),'-'*10,id(tuple1))
tuple2 = tuple(tuple1)
print(f'{tuple2 = }',type(tuple2),'-'*10,id(tuple2))
# tuple类型的数据无法被赋值或被替换
# tuple2[0] = 99
# print(f'{tuple2 = }',type(tuple2),'-'*10,id(tuple2))

#  细节 (元组中仅有单个元素, 需要在元素之后添加逗号, 不能省略)
tuple3 = (1)
print(tuple3, type(tuple3))
tuple4 = (1, )
print(tuple4, type(tuple4))

print('----'*30)
# 字典类型 dict()
'''
 字典类型 : key-value 键值对, 通过 key 实现操作, key 要保证唯⼀性
 Java : Map 接⼝ HashMap / LinkedHashMap 哈希表
 Python : dict() {key: value}
'''

# keys()与values()与items()
dict1 = {'a':1,'b':2,'c':3}
print(f'{dict1 = }',type(dict1),'-'*10,id(dict1))
print(f'{dict1.keys() = }',type(dict1.keys()))
print(f'{dict1.values() = }',type(dict1.values()))
print(f'{dict1.items() = }',type(dict1.items()))

# 通过键进行值的替换
dict1['a'] = 100
print(f'{dict1 = }',type(dict1),'-'*10,id(dict1))

# 通过键查询值
result1 = dict1['a']
print(f'{result1 = }',type(result1),'-'*10,id(result1))


# 集合 三大特性
# 1.确定性
# 2.无序性
# 3.互异性

# 定义一个集合
aset = {1,2,3,4,5,6,7,8,9}
print(f'{aset = }',type(aset),'-'*10,id(aset))

bset = set({1,2,3,4,5,6,7,8,9})
print(f'{bset = }',type(bset),'-'*10,id(bset))

# 综合练习
a = set((range(5,19)))
print(f'{a = }',type(a),'-'*10,id(a))
b = set(range(14))
print(f'{b = }',type(b),'-'*10,id(b))

# 交集 intersection()  或  &
t1 = a.intersection(b)
print(f'{t1 = }',type(t1),'-'*10,id(t1))
t2 = a & b
print(f'{t2 = }',type(t2),'-'*10,id(t2))
print('----'*30)
# 并集 union()  或  |
t3 = a.union(b)
print(f'{t3 = }',type(t3),'-'*10,id(t3))
t4 = a | b
print(f'{t4 = }',type(t4),'-'*10,id(t4))
print('----'*30)
# 差集 difference()  或  -
t5 = a.difference(b)
print(f'{t5 = }',type(t5),'-'*10,id(t5))
t6 = a - b
print(f'{t6 = }',type(t6),'-'*10,id(t6))
t7 = b -a
print(f'{t7 = }',type(t7),'-'*10,id(t7))

# 对称差集 symmetric_difference()  或  ^
t8 = a.symmetric_difference(b)
print(f'{t8 = }',type(t8),'-'*10,id(t8))
t9 = a ^ b
print(f'{t9 = }',type(t9),'-'*10,id(t9))

# 等于  ==
print(f'{a == b = }')
# 不等于  !=
print(f'{a != b = }')
# in  in()
print(f'{1 in a = }')
print(f'{1 in b = }')
# not in  not in
print(f'{1 not in a = }')
print(f'{1 not in b = }')
