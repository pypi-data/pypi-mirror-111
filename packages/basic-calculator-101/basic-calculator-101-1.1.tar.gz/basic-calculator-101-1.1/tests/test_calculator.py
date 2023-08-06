from calculator.calculator import Calculator

#Arrange(setting anything that needs to go before the action happens)
calculator = Calculator()


def test_add():
     #Act
    result = calculator.add(2)
     #Assert (main one)
    assert result == 2
     
def test_subtract():
    assert calculator.subtract(9) == -7

def test_multiply():
    assert calculator.multiply(2) == -14

def test_divide():
    assert calculator.divide(2) == -7

def test_nth_root():
    assert calculator.nth_root(1) == -7

def test_reset_memory():
    assert calculator.reset_memory() == 0
