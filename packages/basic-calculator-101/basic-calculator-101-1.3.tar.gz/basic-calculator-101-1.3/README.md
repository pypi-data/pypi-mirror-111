# Calculator

## Project Motivation
The aim of the project is to build a simple python package with basic functions: add, subtract, multiply, divide and nth root. Also an ability to reset to zero.

## Setup
- to use the package in your notebook:
```python
!pip install basic-calculator-101==1.3

from calculator.calculator import Calculator
```

## Features with Code Examples
```python
calculator = Calculator()

Addition: calculator.add(6)
Subtraction: calculator.subtract(3)
Multiplication: calculator.multiply(2)
Division: calculator.divide(5)
Take (n) root of number: calculator.nth_root(16)
Memory of last result: calculator.reset_memory()
```
## License
This project is licensed under the terms of the **MIT** [license](https://opensource.org/licenses/MIT).

## Acknowledgements
Turing College