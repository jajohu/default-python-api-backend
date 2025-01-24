import datetime
import pytest
from app.models.message import Message
from app.usage_strategies.text_message import TextMessageUsageStrategy


def test_base_cost():
    """Every message should have a base cost of 1 credit."""
    strategy = TextMessageUsageStrategy()
    assert strategy.calculate_usage(Message(
        id=1,
        text="hi",
        timestamp=datetime.datetime(2024, 1, 1)
    )).usage == TextMessageUsageStrategy.BASE_COST


def test_character_count():
    """Every character adds 0.05 credits to total cost."""
    # Repetition to eliminate uniqueness bonus
    test_text = "xxzx xzxx xxxx xxxz xxzx"
    strategy = TextMessageUsageStrategy()
    expected = TextMessageUsageStrategy.BASE_COST + (TextMessageUsageStrategy.CHAR_COST * len(test_text.replace(" ", ""))) + (TextMessageUsageStrategy.LENGTH_4_7 * len(test_text.split(" ")))
    assert pytest.approx(strategy.calculate_usage(Message(
        id=1,
        text=test_text,  
        timestamp=datetime.datetime(2024, 1, 1)
    )).usage) == pytest.approx(expected)


def test_word_length_multipliers():
    """Different word lengths have different costs."""
    cat = "cat"  # 3 chars -> 0.1
    dogs = "dogs"  # 4 chars -> 0.2
    elephants = "elephants"  # 9 chars -> 0.3
    test_text = f"{cat} {cat} {dogs} {elephants}"
    strategy = TextMessageUsageStrategy()
    expected = TextMessageUsageStrategy.BASE_COST + TextMessageUsageStrategy.LENGTH_1_3 + TextMessageUsageStrategy.LENGTH_1_3 + TextMessageUsageStrategy.LENGTH_4_7 + TextMessageUsageStrategy.LENGTH_8_PLUS + (TextMessageUsageStrategy.CHAR_COST * len(test_text.replace(" ", "")))
    assert pytest.approx(strategy.calculate_usage(Message(
        id=1,
        text=test_text,
        timestamp=datetime.datetime(2024, 1, 1)
    )).usage) == pytest.approx(expected)


def test_third_vowel_positions():
    """Vowels in positions divisible by 3 cost extra."""
    test_text = "sleep sleep"
    strategy = TextMessageUsageStrategy()
    expected = TextMessageUsageStrategy.BASE_COST + (TextMessageUsageStrategy.LENGTH_4_7 * 2) + (TextMessageUsageStrategy.THIRD_VOWEL_COST * 2) + (TextMessageUsageStrategy.CHAR_COST * len(test_text.replace(" ", "")))
    assert strategy.calculate_usage(Message(
        id=1,
        text=test_text,
        timestamp=datetime.datetime(2024, 1, 1)
    )).usage == expected


def test_length_penalty():
    """Messages over 100 characters get a penalty."""
    test_text = "xyz" * 101
    strategy = TextMessageUsageStrategy()
    expected = TextMessageUsageStrategy.BASE_COST + TextMessageUsageStrategy.LENGTH_PENALTY + (TextMessageUsageStrategy.CHAR_COST * len(test_text)) - TextMessageUsageStrategy.UNIQUE_BONUS
    assert strategy.calculate_usage(Message(
        id=1,
        text=test_text,
        timestamp=datetime.datetime(2024, 1, 1)
    )).usage == expected


def test_unique_word_bonus():
    """All unique words subtract 2 credits from total."""
    test_text = "bbb ccc ddd fff ggg hhh jjj kkk lll mmm nnn ppp"
    strategy = TextMessageUsageStrategy()
    expected = TextMessageUsageStrategy.BASE_COST + (TextMessageUsageStrategy.LENGTH_1_3 * len(test_text.split())) + (TextMessageUsageStrategy.CHAR_COST * len(test_text.replace(" ", ""))) - TextMessageUsageStrategy.UNIQUE_BONUS
    assert pytest.approx(strategy.calculate_usage(Message(
        id=1,
        text=test_text,
        timestamp=datetime.datetime(2024, 1, 1)
    )).usage) == pytest.approx(expected)


def test_palindrome():
    """Palindromes double the total cost."""
    test_text = "a Santa lived as a devil at NASA"
    strategy = TextMessageUsageStrategy()
    char_count = len(test_text.replace(" ", ""))
    base_cost = TextMessageUsageStrategy.BASE_COST + (TextMessageUsageStrategy.LENGTH_4_7 * 4) + (TextMessageUsageStrategy.LENGTH_1_3 * 4) + (TextMessageUsageStrategy.CHAR_COST * char_count) + (TextMessageUsageStrategy.THIRD_VOWEL_COST * 4)
    assert pytest.approx(strategy.calculate_usage(Message(
        id=1,
        text=test_text,
        timestamp=datetime.datetime(2024, 1, 1)
    )).usage) == pytest.approx(base_cost * 2)
