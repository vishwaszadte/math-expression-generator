import pytest
from math_expression_generator import ExpGenerator


class TestBase:
    """Base class for test cases providing common functionality."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup fixture that runs automatically for all test methods."""
        self.generator = ExpGenerator()

    def _extract_numbers(self, expression: str) -> list[int]:
        """Helper method to extract numbers from expression."""
        return [int(n) for n in expression.split() if n.isdigit()]

    def _extract_operators(self, expression: str) -> list[str]:
        """Helper method to extract operators from expression."""
        return [op for op in expression.split() if op in "+-*/"]

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
        assert all(
            isinstance(expr, str) and isinstance(res, (int, float))
            for expr, res in expressions
        )

    def test_expression_set_difficulty(self):
        """Test that all expressions in a set maintain the specified difficulty."""
        difficulty = 1
        expressions = self.generator.generate_expression_set(
            count=3, difficulty=difficulty
        )
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
            if "/" in expression:
                assert float(result).is_integer()

    def test_no_zero_division(self):
        """Test that division by zero never occurs."""
        for _ in range(20):  # Test multiple times due to randomness
            expression, _ = self.generator.generate_expression()
            if "/" in expression:
                parts = expression.split()
                division_indices = [i for i, part in enumerate(parts) if part == "/"]
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
        assert all(parts[i] in "+-*/" for i in range(1, len(parts), 2))

    def test_result_type(self):
        """Test that results are always numbers."""
        _, result = self.generator.generate_expression()
        assert isinstance(result, (int, float))

    @pytest.mark.parametrize(
        "difficulty,min_value,max_value",
        [
            (1, 0, 9),
            (2, 10, 99),
            (3, 100, 999),
        ],
    )
    def test_number_ranges(self, difficulty, min_value, max_value):
        """Test that numbers are within the expected range for each difficulty."""
        expression, _ = self.generator.generate_expression(difficulty=difficulty)
        numbers = self._extract_numbers(expression)
        assert any(min_value <= n <= max_value for n in numbers)


class TestOperandCount(TestBase):
    """Test cases for operand count functionality."""

    @pytest.mark.parametrize(
        "min_ops,max_ops",
        [
            (2, 5),  # default
            (3, 7),
            (4, 4),  # fixed number
            (2, 10),
        ],
    )
    def test_operand_range_initialization(self, min_ops, max_ops):
        """Test initialization with different operand ranges."""
        generator = ExpGenerator(min_operands=min_ops, max_operands=max_ops)
        assert generator.min_operands == min_ops
        assert generator.max_operands == max_ops

    def test_default_random_operands(self):
        """Test that default random operands stay within range."""
        for _ in range(50):  # Test multiple times
            expression, _ = self.generator.generate_expression()
            operand_count = self._count_operands(expression)
            assert 2 <= operand_count <= 5

    def test_specific_operand_count(self):
        """Test expression generation with specific operand count."""
        for count in range(2, 6):
            expression, _ = self.generator.generate_expression(num_operands=count)
            assert self._count_operands(expression) == count

    @pytest.mark.parametrize("invalid_count", [-1, 0, 1])
    def test_invalid_operand_count(self, invalid_count):
        """Test that invalid operand counts raise ValueError."""
        with pytest.raises(ValueError):
            self.generator.generate_expression(num_operands=invalid_count)

    def test_custom_range_random_operands(self):
        """Test random operands within custom range."""
        generator = ExpGenerator(min_operands=3, max_operands=4)
        for _ in range(20):
            expression, _ = generator.generate_expression()
            operand_count = self._count_operands(expression)
            assert 3 <= operand_count <= 4


class TestDecimalResults(TestBase):
    """Test cases for decimal result functionality."""

    @pytest.fixture
    def decimal_generator(self):
        """Fixture for generator that allows decimal results."""
        return ExpGenerator(allow_decimal_result=True)

    def test_division_with_decimals(self, decimal_generator):
        """Test that division can produce decimal results when allowed."""
        found_decimal = False
        for _ in range(20):  # Try multiple times to get a decimal result
            _, result = decimal_generator.generate_expression()
            if isinstance(result, float) and not result.is_integer():
                found_decimal = True
                break
        assert found_decimal, "No decimal results found in 20 attempts"

    def test_decimal_precision(self, decimal_generator):
        """Test that decimal results are rounded to 2 places."""
        for _ in range(20):
            _, result = decimal_generator.generate_expression()
            if isinstance(result, float):
                # Convert to string and check decimal places
                decimal_str = str(result).split(".")
                if len(decimal_str) > 1:  # If there are decimal places
                    assert len(decimal_str[1]) <= 2

    def test_no_decimals_when_disabled(self):
        """Test that decimal results don't occur when not allowed."""
        decimal_generator = ExpGenerator(allow_decimal_result=False)
        for _ in range(20):
            exp, result = decimal_generator.generate_expression()
            print(f" Expression {exp} Result {result}")
            assert isinstance(result, (int, float))
            assert float(result).is_integer()


class TestNegativeResults(TestBase):
    """Test cases for negative result functionality."""

    @pytest.fixture
    def negative_generator(self):
        """Fixture for generator that allows negative results."""
        return ExpGenerator(allow_negative_result=True)

    def test_negative_results_when_allowed(self, negative_generator):
        """Test that negative results can occur when allowed."""
        found_negative = False
        for _ in range(30):  # Try multiple times to get a negative result
            _, result = negative_generator.generate_expression()
            if result < 0:
                found_negative = True
                break
        assert found_negative, "No negative results found in 30 attempts"

    def test_no_negatives_when_disabled(self):
        """Test that negative results don't occur when not allowed."""
        generator = ExpGenerator(allow_negative_result=False)
        for _ in range(20):
            _, result = generator.generate_expression()
            assert result >= 0

    def test_subtraction_handling_with_negatives_disabled(self):
        """Test that subtraction is properly handled when negatives are disabled."""
        generator = ExpGenerator(allow_negative_result=False)
        for _ in range(20):
            expression, result = generator.generate_expression()
            # If there's subtraction, verify result is still non-negative
            if "-" in expression:
                assert result >= 0


class TestCombinedFeatures(TestBase):
    """Test cases for combinations of features."""

    @pytest.fixture
    def full_featured_generator(self):
        """Fixture for generator with all features enabled."""
        return ExpGenerator(
            min_operands=3,
            max_operands=6,
            allow_decimal_result=True,
            allow_negative_result=True,
        )

    def test_decimal_and_negative(self, full_featured_generator):
        """Test combinations of decimal and negative results."""
        results = []
        for _ in range(50):
            _, result = full_featured_generator.generate_expression()
            results.append(result)

        # Check if we got both decimal and negative results
        has_decimal = any(isinstance(r, float) and not r.is_integer() for r in results)
        has_negative = any(r < 0 for r in results)

        assert has_decimal, "No decimal results found"
        assert has_negative, "No negative results found"

    def test_operand_count_with_features(self, full_featured_generator):
        """Test operand count constraints with other features enabled."""
        for _ in range(20):
            expression, _ = full_featured_generator.generate_expression()
            operand_count = self._count_operands(expression)
            assert 3 <= operand_count <= 6

    @pytest.mark.parametrize("difficulty", [1, 2, 3])
    def test_all_features_with_difficulty(self, full_featured_generator, difficulty):
        """Test that difficulty levels work with all features enabled."""
        expression, _ = full_featured_generator.generate_expression(
            difficulty=difficulty
        )
        numbers = self._extract_numbers(expression)
        max_value = 10**difficulty - 1
        assert all(n <= max_value for n in numbers)


class TestEdgeCases(TestBase):
    """Test cases for edge cases and special scenarios."""

    def test_consecutive_divisions(self):
        """Test expressions with consecutive division operations."""
        generator = ExpGenerator(allow_decimal_result=True, allow_negative_result=True)
        expression, result = generator.generate_expression(num_operands=4)
        if expression.count("/") > 1:
            assert isinstance(result, (int, float))
            if not generator.allow_decimal_result:
                assert float(result).is_integer()

    def test_max_difficulty_with_features(self):
        """Test maximum difficulty with all features enabled."""
        generator = ExpGenerator(
            max_difficulty=4, allow_decimal_result=True, allow_negative_result=True
        )
        expression, _ = generator.generate_expression(difficulty=4)
        numbers = self._extract_numbers(expression)
        assert any(n >= 1000 for n in numbers)


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
