class BankAccount:
    """银行账户类 - 封装示例"""

    def __init__(self, account_number, account_name, initial_balance=0):
        # 公有属性（可以直接访问）
        self.account_number = account_number
        self.account_name = account_name

        # 私有属性（使用双下划线开头，不能直接访问）
        self.__balance = initial_balance
        self.__transaction_history = []

        # 记录初始交易
        if initial_balance > 0:
            self.__add_transaction("开户", initial_balance)

    # 私有方法（只能在类内部使用）
    def __add_transaction(self, trans_type, amount):
        """添加交易记录"""
        self.__transaction_history.append({
            'type': trans_type,
            'amount': amount,
            'balance': self.__balance
        })

    # 公有方法 - 获取余额（getter方法）
    def get_balance(self):
        """查询余额"""
        return self.__balance

    # 公有方法 - 存款
    def deposit(self, amount):
        """存款"""
        if amount <= 0:
            raise ValueError("存款金额必须大于0")

        self.__balance += amount
        self.__add_transaction("存款", amount)
        print(f"存款成功！存入：{amount}元，当前余额：{self.__balance}元")
        return True

    # 公有方法 - 取款
    def withdraw(self, amount):
        """取款"""
        if amount <= 0:
            raise ValueError("取款金额必须大于0")

        if amount > self.__balance:
            print(f"余额不足！当前余额：{self.__balance}元")
            return False

        self.__balance -= amount
        self.__add_transaction("取款", -amount)
        print(f"取款成功！取出：{amount}元，当前余额：{self.__balance}元")
        return True

    # 公有方法 - 查看交易记录
    def show_transaction_history(self):
        """显示交易记录"""
        print(f"\n账户：{self.account_name}({self.account_number})的交易记录：")
        print("-" * 50)
        for trans in self.__transaction_history:
            print(f"类型：{trans['type']:4s}  金额：{trans['amount']:8.2f}  余额：{trans['balance']:8.2f}")
        print("-" * 50)

    # 属性装饰器（更优雅的getter/setter）
    @property
    def balance(self):
        """通过属性方式访问余额"""
        return self.__balance

    @balance.setter
    def balance(self, value):
        """禁止直接修改余额"""
        raise AttributeError("不能直接修改余额，请使用deposit或withdraw方法")

    # 类方法：显示银行信息
    @classmethod
    def bank_info(cls):
        """银行信息"""
        return "欢迎使用Python银行系统"

    # 静态方法：验证金额
    @staticmethod
    def validate_amount(amount):
        """验证金额是否合法"""
        return isinstance(amount, (int, float)) and amount > 0


# 使用示例
if __name__ == "__main__":
    # 创建账户
    account = BankAccount("10086", "张三", 0)

    # 访问公有属性
    print(f"账户名：{account.account_name}")
    print(f"账号：{account.account_number}")

    # 尝试直接访问私有属性（会报错）
    # print(account.__balance)  # AttributeError

    # 通过公有方法访问
    print(f"当前余额：{account.get_balance()}元")

    # 使用property装饰器访问
    print(f"当前余额（property）：{account.balance}元")

    # 执行操作
    account.deposit(500)
    account.withdraw(200)
    account.withdraw(2000)  # 余额不足

    # 查看交易记录
    account.show_transaction_history()

    # 尝试直接修改余额（会报错）
    # account.balance = 9999  # AttributeError

    # 使用类方法和静态方法
    print(f"\n{BankAccount.bank_info()}")
    print(f"金额100是否合法：{BankAccount.validate_amount(100)}")
    print(f"金额-50是否合法：{BankAccount.validate_amount(-50)}")