from typing import List
import random

def generate_number(difficulty: int) -> int:
    """Generate a random number based on difficulty level."""
    max_value = 10 ** difficulty - 1
    min_value = 10 ** (difficulty - 1) if difficulty > 1 else 0
    return random.randint(min_value, max_value)

def find_divisors(number: int) -> List[int]:
    """Find all divisors of a given number."""
    return [n for n in range(1, number + 1) if number % n == 0]

def validate_difficulty(difficulty: int, max_difficulty: int) -> None:
    """Validate difficulty level."""
    if difficulty < 1 or difficulty > max_difficulty:
        raise ValueError(f"Difficulty must be between 1 and {max_difficulty}")
