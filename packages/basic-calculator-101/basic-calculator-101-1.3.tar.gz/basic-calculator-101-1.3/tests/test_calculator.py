import pytest
from calculator.calculator import Calculator


def test_add():
    #Arrange(setting anything that needs to go before the action happens)
    calculator = Calculator(2)
     #Act
    result = calculator.add(2)
     #Assert (main one)
    assert result == 4
     
def test_subtract():
    calculator = Calculator(2)
    assert calculator.subtract(9) == -7

def test_multiply():
    calculator = Calculator(7)
    assert calculator.multiply(2) == 14

def test_divide():
    calculator = Calculator(14)
    assert calculator.divide(-2) == -7

def test_zero_division():
    with pytest.raises(Exception):
        calculator = Calculator(14)
        calculator.divide(0)

def test_check_operand():
    with pytest.raises(Exception):
        Calculator().add("10")

def test_nth_root():
    calculator = Calculator(16)
    assert calculator.nth_root(2) == 4

def test_reset_memory():
    calculator = Calculator()
    assert calculator.reset_memory() == 0
