# File: src/math_expression_generator/generator.py
from typing import Union, List, Tuple, Optional
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
    
    def __init__(
        self,
        max_difficulty: int = 4,
        min_operands: int = 2,
        max_operands: int = 5,
        allow_decimal_result: bool = False,
        allow_negative_result: bool = False
    ):
        """
        Initialize the generator.
        
        Args:
            max_difficulty: Maximum difficulty level (1-4)
            min_operands: Minimum number of operands in expression (default: 2)
            max_operands: Maximum number of operands in expression (default: 5)
            allow_decimal_result: Whether to allow decimal results (default: False)
            allow_negative_result: Whether to allow negative results (default: False)
        """
        self.max_difficulty = max_difficulty
        self.min_operands = max(2, min_operands)  # Ensure at least 2 operands
        self.max_operands = max(self.min_operands, max_operands)
        self.allow_decimal_result = allow_decimal_result
        self.allow_negative_result = allow_negative_result
        self.operators = Operator.get_all_operators()
    
    def _ensure_valid_division(
        self,
        numbers: List[int],
        operators: List[Operator]
    ) -> Tuple[List[int], List[Operator]]:
        """Ensure division operations follow constraints."""
        for i, op in enumerate(operators):
            if op.type == OperatorType.DIVISION:
                while numbers[i + 1] == 0 or (
                    not self.allow_decimal_result and 
                    numbers[i] % numbers[i + 1] != 0
                ):
                    if self.allow_decimal_result:
                        # If decimals are allowed, just avoid zero division
                        numbers[i + 1] = generate_number(1)  # Use small numbers for cleaner decimals
                        if numbers[i + 1] == 0:  # Ensure no zero division
                            numbers[i + 1] = 1
                    else:
                        # Find valid divisors for whole number results
                        divisors = find_divisors(numbers[i])
                        if not divisors:
                            operators[i] = next(
                                op for op in self.operators 
                                if op.type == OperatorType.MULTIPLICATION
                            )
                            break
                        numbers[i + 1] = random.choice(divisors)
        return numbers, operators
    
    def _ensure_non_negative(
        self,
        numbers: List[int],
        operators: List[Operator]
    ) -> Tuple[List[int], List[Operator]]:
        """Ensure the expression result is non-negative if required."""
        if not self.allow_negative_result:
            # Calculate the result step by step
            result = numbers[0]
            for i, operator in enumerate(operators):
                next_result = operator.func(result, numbers[i + 1])
                # If result would be negative, change the operator
                if next_result < 0:
                    if operator.type == OperatorType.SUBTRACTION:
                        # Change subtraction to addition
                        operators[i] = next(
                            op for op in self.operators 
                            if op.type == OperatorType.ADDITION
                        )
                    result = operators[i].func(result, numbers[i + 1])
                else:
                    result = next_result
        return numbers, operators
    
    def generate_expression(
        self,
        num_operands: Optional[int] = None,
        difficulty: int = 1
    ) -> Tuple[str, float]:
        """
        Generate a random mathematical expression.
        
        Args:
            num_operands: Number of operands (default: random between min_operands and max_operands)
            difficulty: Difficulty level (default: 1)
        
        Returns:
            Tuple of (expression string, result)
        """
        validate_difficulty(difficulty, self.max_difficulty)
        
        if num_operands is None:
            num_operands = random.randint(self.min_operands, self.max_operands)
        else:
            if num_operands < self.min_operands:
                raise ValueError(f"Number of operands must be at least {self.min_operands}")
            if num_operands > self.max_operands:
                raise ValueError(f"Number of operands cannot exceed {self.max_operands}")
        
        numbers = [generate_number(difficulty) for _ in range(num_operands)]
        operators = [random.choice(self.operators) for _ in range(num_operands - 1)]
        
        # Apply constraints
        numbers, operators = self._ensure_valid_division(numbers, operators)
        numbers, operators = self._ensure_non_negative(numbers, operators)
        
        # Build expression and calculate result
        expression = str(numbers[0])
        result = numbers[0]
        
        for i, operator in enumerate(operators):
            expression += f" {operator} {numbers[i + 1]}"
            result = operator.func(result, numbers[i + 1])
            
            # Round decimal results to 2 places for cleaner output
            if isinstance(result, float) and self.allow_decimal_result:
                result = round(result, 2)
        
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