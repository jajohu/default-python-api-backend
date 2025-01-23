import re
from typing import List
from app.models.message import Message
from app.usage_strategies.base import UsageStrategy


class TextMessageUsageStrategy(UsageStrategy):
    BASE_COST = 1
    CHAR_COST = 0.05
    LENGTH_1_3 = 0.1 
    LENGTH_4_7 = 0.2
    LENGTH_8_PLUS = 0.3
    THIRD_VOWEL_COST = 0.3
    LENGTH_PENALTY = 5.0
    UNIQUE_BONUS = 2.0
    VOWELS = "aeiou"

    def __init__(self, message: Message):
        super().__init__(message)
        self.cost = self.BASE_COST

    def calculate_usage(self) -> float:
        words = self._message.text.split(" ")
        self._add_char_cost()
        self._add_word_len_cost(words)
        self._add_third_vowels_cost()
        self._add_length_penalty()
        self._add_uniqueness_bonus(words)
        self._add_palindrome_cost()

        return max(self.BASE_COST, self.cost)
    
    def _add_char_cost(self):
        chars = len(self._message.text.replace(" ", ""))
        self.cost += (self.CHAR_COST * chars)

    def _add_word_len_cost(self, words: List[str]):
        for word in words:
            if 1 <= len(word) <= 3: self.cost += self.LENGTH_1_3
            elif 4 <= len(word) <= 7: self.cost += self.LENGTH_4_7
            elif len(words) >= 8: self.cost += self.LENGTH_8_PLUS

    def _add_third_vowels_cost(self):
        third_vowels = [char for i, char in enumerate(self._message.text) if (i + 1) % 3 == 0 and char in self.VOWELS]
        self.cost += self.THIRD_VOWEL_COST * len(third_vowels)

    def _add_length_penalty(self):
        if len(self._message.text) > 100: self.cost += self.LENGTH_PENALTY

    def _add_uniqueness_bonus(self, words: List[str]):
        if len(words) == len(set(words)): self.cost -= self.UNIQUE_BONUS

    def _add_palindrome_cost(self):
        text_alphanumeric = "".join([char.lower() for char in self._message.text if char.isalnum()])
        if text_alphanumeric[::-1] == text_alphanumeric: self.cost *= 2