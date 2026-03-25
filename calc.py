from logging import raiseExceptions


def add(num1: int, num2: int):
    return num1 + num2

def subtract(num1: int, num2: int):
    return num1 - num2

def multiply(num1: int, num2: int):
    return num1 * num2

def divide(num1: int, num2: int):
    return num1 / num2

class Insufficent_funds(Exception):
    pass

class Bankaccount():
    def __init__(self,start=0):
        self.balance=start
    def deposit(self,amount):
        self.balance+=amount
    def withdraw(self,amount):
        if amount>self.balance:
            raise Insufficent_funds("insufficent funds in account")
            pass
        self.balance-=amount     
    def collect_intrest(self):
        self.balance*=1.1     