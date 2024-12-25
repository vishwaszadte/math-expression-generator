from enum import Enum
from typing import Callable, List
import operator


class OperatorType(Enum):
    """Enum of supported operator types."""
    ADDITION = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "*"
    DIVISION = "/"


class Operator:
    """Class representing a mathematical operator."""

    _OPERATOR_FUNCS = {
        OperatorType.ADDITION: operator.add,
        OperatorType.SUBTRACTION: operator.sub,
        OperatorType.MULTIPLICATION: operator.mul,
        OperatorType.DIVISION: operator.truediv
    }

    def __init__(self, operator_type: OperatorType):
        self.type = operator_type
        self.func = self._OPERATOR_FUNCS[operator_type]
        self.symbol = operator_type.value

    @classmethod
    def get_all_operators(cls) -> List['Operator']:
        """Return list of all available operators."""
        return [cls(op_type) for op_type in OperatorType]

    def __str__(self) -> str:
        return self.symbol
