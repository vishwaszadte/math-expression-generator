from typing import List, Tuple, Optional
import random
from .operators import Operator, OperatorType
from .utils import generate_number, find_divisors, validate_difficulty


class MathExpressionGenerator:
    def __init__(
        self,
        max_difficulty: int = 4,
        min_operands: int = 2,
        max_operands: int = 5,
        allow_decimal_result: bool = False,
        allow_negative_result: bool = False,
        decimal_places: int = 2,  # Add decimal places parameter
    ):
        self.max_difficulty = max_difficulty
        self.min_operands = max(2, min_operands)
        self.max_operands = max(self.min_operands, max_operands)
        self.allow_decimal_result = allow_decimal_result
        self.allow_negative_result = allow_negative_result
        self.decimal_places = decimal_places
        self.operators = Operator.get_all_operators()

    def _evaluate_with_precedence(
        self, numbers: List[int], operators: List[Operator]
    ) -> float:
        """
        Evaluate the expression respecting operator precedence (PEMDAS).
        """
        # First pass: handle multiplication and division
        values = numbers.copy()
        ops = operators.copy()
        i = 0

        while i < len(ops):
            if ops[i].type in (OperatorType.MULTIPLICATION, OperatorType.DIVISION):
                # Apply multiplication or division
                left = values[i]
                right = values[i + 1]
                result = ops[i].func(left, right)
                # Round intermediate results to prevent floating point errors
                if isinstance(result, float):
                    result = round(result, self.decimal_places)

                # Replace the two numbers with their result
                values[i : i + 2] = [result]
                # Remove the used operator
                ops.pop(i)
            else:
                i += 1

        # Second pass: handle addition and subtraction
        result = values[0]
        for i, op in enumerate(ops):
            result = op.func(result, values[i + 1])
            # Round intermediate results
            if isinstance(result, float):
                result = round(result, self.decimal_places)

        return result

    def _is_valid_result(self, result: float) -> bool:
        """
        Check if a result is valid according to current constraints.
        """
        if not self.allow_decimal_result and not float(result).is_integer():
            return False
        if not self.allow_negative_result and result < 0:
            return False
        return True

    def _ensure_valid_division(
        self, numbers: List[int], operators: List[Operator]
    ) -> Tuple[List[int], List[Operator]]:
        """Ensure division operations follow constraints."""
        for i in range(len(operators)):
            if operators[i].type == OperatorType.DIVISION:
                # Handle division by zero
                if numbers[i + 1] == 0:
                    numbers[i + 1] = 1
                    continue

                # Calculate result up to this point with proper precedence
                temp_numbers = numbers[: i + 2]
                temp_operators = operators[: i + 1]
                current_result = self._evaluate_with_precedence(
                    temp_numbers, temp_operators
                )

                if not self.allow_decimal_result:
                    attempts = 0
                    valid_division_found = False

                    while attempts < 10 and not valid_division_found:
                        if float(current_result).is_integer():
                            divisors = find_divisors(int(abs(current_result)))
                            if divisors:
                                numbers[i + 1] = random.choice(divisors)
                                valid_division_found = True
                                break

                        if attempts == 9:
                            # If we can't find a good divisor, change to multiplication
                            operators[i] = next(
                                op
                                for op in self.operators
                                if op.type == OperatorType.MULTIPLICATION
                            )
                        attempts += 1
                        current_result = self._evaluate_with_precedence(
                            temp_numbers, temp_operators
                        )

            # Validate intermediate result with proper precedence
            temp_result = self._evaluate_with_precedence(
                numbers[: i + 2], operators[: i + 1]
            )
            if not self._is_valid_result(temp_result):
                raise ValueError("Invalid intermediate result")

        return numbers, operators

    def generate_expression(
        self, num_operands: Optional[int] = None, difficulty: int = 1
    ) -> Tuple[str, float]:
        validate_difficulty(difficulty, self.max_difficulty)

        if num_operands is None:
            num_operands = random.randint(self.min_operands, self.max_operands)
        else:
            if num_operands < self.min_operands:
                raise ValueError(
                    f"Number of operands must be at least {self.min_operands}"
                )
            if num_operands > self.max_operands:
                raise ValueError(
                    f"Number of operands cannot exceed {self.max_operands}"
                )

        max_attempts = 100
        attempt = 0

        while attempt < max_attempts:
            try:
                numbers = [generate_number(difficulty) for _ in range(num_operands)]
                operators = [
                    random.choice(self.operators) for _ in range(num_operands - 1)
                ]

                # Apply constraints
                numbers, operators = self._ensure_valid_division(numbers, operators)

                # Build expression
                expression = str(numbers[0])
                for i, operator in enumerate(operators):
                    expression += f" {operator} {numbers[i + 1]}"

                # Calculate final result with proper precedence
                result = self._evaluate_with_precedence(numbers, operators)

                # Validate final result
                if not self._is_valid_result(result):
                    raise ValueError("Invalid final result")

                # Round result if it's a decimal
                if isinstance(result, float):
                    if self.allow_decimal_result:
                        result = round(result, self.decimal_places)
                    elif result.is_integer():
                        result = int(result)
                    else:
                        raise ValueError("Invalid decimal result")

                return expression, result

            except ValueError:
                attempt += 1
                continue

        raise ValueError("Could not generate valid expression after maximum attempts")

    def generate_expression_set(
        self, count: int, num_operands: Optional[int] = None, difficulty: int = 1
    ) -> List[Tuple[str, float]]:
        return [
            self.generate_expression(num_operands, difficulty) for _ in range(count)
        ]
