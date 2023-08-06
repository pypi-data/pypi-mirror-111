import numbers

class CalculatorError(Exception):
    """An exception class for Calculator, for errors"""

class Calculator():

    def __init__(self, value=0) -> None:
        self.memory = value
    
    def reset_memory(self):
        """Resets memory to zero."""
        self.memory = 0
        return self.memory

    def add(self, a: float) -> float:
        self._check_operand(a)
        self.memory += a
        return self.memory

    def subtract(self, a: float) -> float:
        self._check_operand(a)
        self.memory -= a
        return self.memory

    def multiply(self, a: float) -> float:
        self._check_operand(a)
        self.memory *= a
        return self.memory

    def divide(self, a: float) -> float:
        self._check_operand(a)
        try:
            self.memory /= a
            return self.memory
        except ZeroDivisionError:
            raise CalculatorError("Cannot divide by 0")

    def nth_root(self, a: float) -> float:
        self._check_operand(a)
        self.memory **= (1/a)
        return self.memory

    def _check_operand(self, operand):
        """Check that the operand is a number."""
        if not isinstance(operand, numbers.Number):
            raise CalculatorError(f'"{operand}" is not a number')

  