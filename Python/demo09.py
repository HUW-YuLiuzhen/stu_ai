"""
面向对象  封装，继承，多态，抽象

作业
设计两个共性的 动物类 与 ⻝物类
动物类⼦类有: 狗类,猫类,⻦类都继承⾃动物类. 有名称属性, 和吃的⾏为.
⻝物类⼦类有 : ⻣头, ⻥, ⾍⼦
最后设计⼀个Person类,拥有喂动物的⾏为

"""

from abc import ABC, abstractmethod

# 创建一个食物父类
class Food(object):
    def __init__(self, name):
        self.name = name.title()

    @property
    def name(self):
        if self.__name:
            return self.__name
        else:
            return "当前无食物"

    @name.setter
    def name(self, name):
        if isinstance(name,str) :
            self.__name = name.title()
        else:
            self.__name = None


# 创建动物父类
class Animal(ABC):
    def __init__(self, name):
        self.name = name.title()

    # 定义一个抽象方法
    @abstractmethod
    def eat(self,food : Food):...

    # 创建get方法
    @property
    def name1(self):
        if self.__name:
            return  self.__name  # __变量 这就是私有属性
        else:
            return '无任何数据'

    # 创建set方法
    @name1.setter
    def name(self,name):
        if isinstance(name,str):
            self.__name = name.title()
        else:
            self.__name = None

# 创建动物子类  进行继承操作
class Dog(Animal):
    def __init__(self,name):
        # 调用父类的构造方法，获取name值
        super().__init__(name)

    def eat(self,food : Food):
        print(f'{self.name} 正在吃 {food.name}')

    def dog_by(self,food : Food):
        print(f'{self.name} 吃完了 {food.name} 后开始摇尾巴了')

# 创建食物子类
class Bone(Food):
    def __init__(self,name):
        super().__init__(name)


# 定义一个人类 进行投喂
class People(object):
    def __init__(self,name):
        self.name = name.title()

    def people_tw(self,animal : Animal,food : Food):  # 通过
        print(f'{self.name} 投喂了 {animal.name} , {animal.name} 正在吃 {food.name}')

        animal.eat(food)

        if isinstance(animal,Dog):
            animal.dog_by(food)


mpeople = People('韩立')

mdog = Dog('汪汪')

mBone = Bone('饼干')
#
mpeople.people_tw(mdog,mBone)