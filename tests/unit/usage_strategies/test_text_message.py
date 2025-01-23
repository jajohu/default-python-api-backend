import datetime
import pytest
from app.models.message import Message
from app.usage_strategies.text_message import TextMessageUsageStrategy

BASE_COST = 1
CHAR_COST = 0.05
LENGTH_1_3 = 0.1
LENGTH_4_7 = 0.2
LENGTH_8_PLUS = 0.3
THIRD_VOWEL_COST = 0.3
LENGTH_PENALTY = 5.0
UNIQUE_BONUS = 2.0


def test_base_cost():
    """Every message should have a base cost of 1 credit."""
    strategy = TextMessageUsageStrategy(Message(
        id=1,
        text="hi",
        timestamp=datetime.datetime(2024, 1, 1)
    ))
    assert strategy.calculate_usage() == BASE_COST


def test_character_count():
    """Every character adds 0.05 credits to total cost."""
    # Repetition to eliminate uniqueness bonus
    test_text = "test test test test test"
    strategy = TextMessageUsageStrategy(Message(
        id=1,
        text=test_text,  
        timestamp=datetime.datetime(2024, 1, 1)
    ))
    expected = BASE_COST + (CHAR_COST * len(test_text.replace(" ", ""))) + LENGTH_4_7 * len(test_text.split())
    assert strategy.calculate_usage() == expected


def test_word_length_multipliers():
    """Different word lengths have different costs."""
    cat = "cat"  # 3 chars -> 0.1
    dogs = "dogs"  # 4 chars -> 0.2
    elephants = "elephants"  # 9 chars -> 0.3
    test_text = f"{cat} {dogs} {elephants}"
    strategy = TextMessageUsageStrategy(Message(
        id=1,
        text=test_text,
        timestamp=datetime.datetime(2024, 1, 1)
    ))
    expected = BASE_COST + LENGTH_1_3 + LENGTH_4_7 + LENGTH_8_PLUS + (CHAR_COST * len(test_text.replace(" ", "")))
    assert strategy.calculate_usage() == expected


def test_third_vowel_positions():
    """Vowels in positions divisible by 3 cost extra."""
    test_text = "sleep sleep"
    strategy = TextMessageUsageStrategy(Message(
        id=1,
        text=test_text,
        timestamp=datetime.datetime(2024, 1, 1)
    ))
    expected = BASE_COST + (LENGTH_4_7 * 2) + (THIRD_VOWEL_COST * 2) + (CHAR_COST * len(test_text.replace(" ", "")))
    assert strategy.calculate_usage() == expected


def test_length_penalty():
    """Messages over 100 characters get a penalty."""
    test_text = "x" * 101
    strategy = TextMessageUsageStrategy(Message(
        id=1,
        text=test_text,
        timestamp=datetime.datetime(2024, 1, 1)
    ))
    expected = BASE_COST + LENGTH_8_PLUS + LENGTH_PENALTY + (CHAR_COST * len(test_text)) - UNIQUE_BONUS
    assert strategy.calculate_usage() == expected


def test_unique_word_bonus():
    """All unique words subtract 2 credits from total."""
    test_text = "the cat sat"
    strategy = TextMessageUsageStrategy(Message(
        id=1,
        text=test_text,
        timestamp=datetime.datetime(2024, 1, 1)
    ))
    expected = BASE_COST + (LENGTH_1_3 * len(test_text.split())) + (CHAR_COST * len(test_text.replace(" ", ""))) - UNIQUE_BONUS
    assert strategy.calculate_usage() == expected


def test_palindrome():
    """Palindromes double the total cost."""
    test_text = "race car"
    strategy = TextMessageUsageStrategy(Message(
        id=1,
        text=test_text,
        timestamp=datetime.datetime(2024, 1, 1)
    ))
    char_count = len(test_text.replace(" ", ""))
    base_cost = BASE_COST + (LENGTH_4_7 * 2) + (CHAR_COST * char_count) - UNIQUE_BONUS
    assert strategy.calculate_usage() == base_cost * 2
