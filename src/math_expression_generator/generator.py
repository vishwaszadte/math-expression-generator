from typing import List, Tuple, Optional
import random
from .operators import Operator, OperatorType
from .utils import (
    generate_number,
    find_divisors,
    validate_difficulty,
    validate_operands_count
)


class MathExpressionGenerator:
    """Generator for random mathematical expressions with customizable difficulty."""

    def __init__(self, max_difficulty: int = 4):
        """
        Initialize the generator.

        Args:
            max_difficulty (int): Maximum difficulty level (1-4)
        """
        self.max_difficulty = max_difficulty
        self.operators = Operator.get_all_operators()

    def _ensure_valid_division(
            self,
            numbers: List[int],
            operators: List[Operator]
    ) -> Tuple[List[int], List[Operator]]:
        """Ensure division operations result in whole numbers."""
        for i, op in enumerate(operators):
            if op.type == OperatorType.DIVISION:
                while numbers[i + 1] == 0 or numbers[i] % numbers[i + 1] != 0:
                    divisors = find_divisors(numbers[i])
                    if not divisors:
                        operators[i] = next(
                            op for op in self.operators
                            if op.type == OperatorType.MULTIPLICATION
                        )
                        break
                    numbers[i + 1] = random.choice(divisors)
        return numbers, operators

    def generate_expression(
            self,
            num_operands: Optional[int] = None,
            difficulty: int = 1
    ) -> Tuple[str, float]:
        """
        Generate a random mathematical expression.

        Args:
            num_operands: Number of operands (default: random 2-5)
            difficulty: Difficulty level (default: 1)

        Returns:
            Tuple of (expression string, result)
        """
        validate_difficulty(difficulty, self.max_difficulty)

        if num_operands is None:
            num_operands = random.randint(2, 5)
        validate_operands_count(num_operands)

        numbers = [generate_number(difficulty) for _ in range(num_operands)]
        operators = [random.choice(self.operators) for _ in range(num_operands - 1)]

        numbers, operators = self._ensure_valid_division(numbers, operators)

        expression = str(numbers[0])
        result = numbers[0]

        for i, operator in enumerate(operators):
            expression += f" {operator} {numbers[i + 1]}"
            result = operator.func(result, numbers[i + 1])

        return expression, result

    def generate_expression_set(
            self,
            count: int,
            num_operands: Optional[int] = None,
            difficulty: int = 1
    ) -> List[Tuple[str, float]]:
        """
        Generate multiple expressions.

        Args:
            count: Number of expressions to generate
            num_operands: Number of operands per expression
            difficulty: Difficulty level

        Returns:
            List of (expression, result) tuples
        """
        return [
            self.generate_expression(num_operands, difficulty)
            for _ in range(count)
        ]
