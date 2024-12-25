A Python package for generating random mathematical expressions with customizable difficulty levels.

## Installation

```bash
pip install git+https://github.com/vishwaszadte/math-expression-generator.git
```

## Usage

```python
from math_expression_generator import ExpGenerator

# Create generator instance
generator = ExpGenerator()

# Generate a single expression
expression, result = generator.generate_expression(difficulty=1)
print(f"{expression} = {result}")

# Generate multiple expressions
expressions = generator.generate_expression_set(count=3, difficulty=2)
for expr, res in expressions:
    print(f"{expr} = {res}")
```

## Features

- Customizable difficulty levels
- Variable number of operands
- Support for basic arithmetic operations (+, -, *, /)
- Ensures valid division operations
- Batch generation of expressions

## License

MIT License
