from calc import Insufficent_funds, add, divide, multiply,subtract,multiply,divide, Bankaccount
import pytest

@pytest.fixture
def zero_account():
    return Bankaccount()

@pytest.fixture
def account():
    return Bankaccount(45)

@pytest.mark.parametrize("num1,num2,result", [
    (2, 4, 6),
    (5, 9, 14),
    (4, 5, 9)
])
def test_add(num1, num2, result):
    assert add(num1, num2) == result

def test_subtract():
    assert subtract(5, 3) == 2

def test_multiply():
    assert multiply(5, 3) == 15

def test_divide():
    assert divide(6, 3) == 2

def test_deposit(zero_account):
    assert zero_account.balance == 0

def test_withdraw(account):
    account.withdraw(40)
    assert account.balance == 5

def test_intrest(account):
    account.collect_intrest()
    assert round(account.balance, 2) == 49.5
@pytest.mark.parametrize("deposit,withdraw,total", [
    (200, 40, 160),
    (500, 9, 491),
    (400, 50,350)
])

def test_bank_trans(zero_account,deposit,withdraw,total):
    zero_account.deposit(deposit)
    zero_account.withdraw(withdraw)
    assert zero_account.balance==total  

def test_insufficent_funds(account):
    with pytest.raises(Insufficent_funds):
        account.withdraw(200)
