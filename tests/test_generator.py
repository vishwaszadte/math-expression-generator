# File: tests/test_generator.py
import pytest
from math_expression_generator import MathExpressionGenerator


class TestBase:
    """Base class for test cases providing common functionality."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup fixture that runs automatically for all test methods."""
        self.generator = MathExpressionGenerator()

    def _extract_numbers(self, expression: str) -> list[int]:
        """Helper method to extract numbers from expression."""
        return [int(n) for n in expression.split() if n.isdigit()]

    def _extract_operators(self, expression: str) -> list[str]:
        """Helper method to extract operators from expression."""
        return [op for op in expression.split() if op in '+-*/']

    def _count_operands(self, expression: str) -> int:
        """Helper method to count operands in expression."""
        return len(self._extract_numbers(expression))


class TestExpressionGeneration(TestBase):
    """Test cases for basic expression generation functionality."""

    def test_single_digit_expression(self):
        """Test that difficulty level 1 generates only single-digit numbers."""
        expression, _ = self.generator.generate_expression(difficulty=1)
        numbers = self._extract_numbers(expression)
        assert all(0 <= n <= 9 for n in numbers)

    def test_double_digit_expression(self):
        """Test that difficulty level 2 generates at least one double-digit number."""
        expression, _ = self.generator.generate_expression(difficulty=2)
        numbers = self._extract_numbers(expression)
        assert any(n >= 10 for n in numbers)

    def test_expression_evaluation(self):
        """Test that the generated result matches actual evaluation."""
        expression, expected_result = self.generator.generate_expression()
        actual_result = eval(expression)  # Safe here as we control the input
        assert actual_result == expected_result

    def test_custom_operands_count(self):
        """Test expression generation with specific number of operands."""
        expression, _ = self.generator.generate_expression(num_operands=3)
        operators = self._extract_operators(expression)
        assert len(operators) == 2  # For 3 operands, there should be 2 operators


class TestExpressionSet(TestBase):
    """Test cases for generating sets of expressions."""

    def test_expression_set_generation(self):
        """Test generating multiple expressions at once."""
        expressions = self.generator.generate_expression_set(count=5)
        assert len(expressions) == 5
        assert all(isinstance(expr, str) and isinstance(res, (int, float))
                   for expr, res in expressions)

    def test_expression_set_difficulty(self):
        """Test that all expressions in a set maintain the specified difficulty."""
        difficulty = 1
        expressions = self.generator.generate_expression_set(count=3, difficulty=difficulty)
        for expression, _ in expressions:
            numbers = self._extract_numbers(expression)
            assert all(0 <= n <= 9 for n in numbers)


class TestValidation(TestBase):
    """Test cases for input validation and error handling."""

    @pytest.mark.parametrize("difficulty", [0, 5, -1])
    def test_invalid_difficulty(self, difficulty):
        """Test that invalid difficulty levels raise ValueError."""
        with pytest.raises(ValueError):
            self.generator.generate_expression(difficulty=difficulty)

    @pytest.mark.parametrize("num_operands", [0, 1, -1])
    def test_invalid_operands_count(self, num_operands):
        """Test that invalid operands count raise ValueError."""
        with pytest.raises(ValueError):
            self.generator.generate_expression(num_operands=num_operands)


class TestOperations(TestBase):
    """Test cases for mathematical operations and their properties."""

    def test_division_validity(self):
        """Test that division operations always result in whole numbers."""
        for _ in range(10):  # Test multiple times due to randomness
            expression, result = self.generator.generate_expression()
            if '/' in expression:
                assert result.is_integer()

    def test_no_zero_division(self):
        """Test that division by zero never occurs."""
        for _ in range(20):  # Test multiple times due to randomness
            expression, _ = self.generator.generate_expression()
            if '/' in expression:
                parts = expression.split()
                division_indices = [i for i, part in enumerate(parts) if part == '/']
                for idx in division_indices:
                    divisor = int(parts[idx + 1])
                    assert divisor != 0


class TestFormatting(TestBase):
    """Test cases for expression formatting and structure."""

    def test_expression_format(self):
        """Test that generated expressions follow the expected format."""
        expression, _ = self.generator.generate_expression()
        parts = expression.split()

        # Check that odd indices are operators and even indices are numbers
        assert all(parts[i].isdigit() for i in range(0, len(parts), 2))
        assert all(parts[i] in '+-*/' for i in range(1, len(parts), 2))

    def test_result_type(self):
        """Test that results are always numbers."""
        _, result = self.generator.generate_expression()
        assert isinstance(result, (int, float))

    @pytest.mark.parametrize("difficulty,min_value,max_value", [
        (1, 0, 9),
        (2, 10, 99),
        (3, 100, 999),
    ])
    def test_number_ranges(self, difficulty, min_value, max_value):
        """Test that numbers are within the expected range for each difficulty."""
        expression, _ = self.generator.generate_expression(difficulty=difficulty)
        numbers = self._extract_numbers(expression)
        assert any(min_value <= n <= max_value for n in numbers)


class TestPerformance(TestBase):
    """Test cases for performance and resource usage."""

    @pytest.mark.performance
    def test_large_expression_set(self):
        """Test generating a large set of expressions."""
        count = 1000
        start_time = pytest.importorskip("time").time()
        expressions = self.generator.generate_expression_set(count=count)
        end_time = pytest.importorskip("time").time()

        assert len(expressions) == count
        assert end_time - start_time < 5  # Should complete within 5 seconds