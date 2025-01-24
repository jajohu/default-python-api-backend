from typing import List
from app.models.message import Message
from app.usage_strategies.base import UsageResult, UsageStrategy


# pylint: disable=R0903
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

    def calculate_usage(self, message: Message) -> UsageResult:
        self._reset_current_usage()
        words = message.text.split(" ")
        self._add_char_cost(message.text)
        self._add_word_len_cost(words)
        self._add_third_vowels_cost(message.text)
        self._add_length_penalty(message.text)
        self._add_uniqueness_bonus(words)
        self._add_palindrome_cost(message.text)

        return UsageResult(
            usage=round(max(self.BASE_COST, self._current_usage), 4), report_name=None
        )

    def _add_char_cost(self, message_text: str):
        chars = len(message_text.replace(" ", ""))
        self._current_usage += self.CHAR_COST * chars

    def _add_word_len_cost(self, words: List[str]):
        for word in words:
            if 1 <= len(word) <= 3:
                self._current_usage += self.LENGTH_1_3
            elif 4 <= len(word) <= 7:
                self._current_usage += self.LENGTH_4_7
            elif len(words) >= 8:
                self._current_usage += self.LENGTH_8_PLUS

    def _add_third_vowels_cost(self, message_text: str):
        third_vowels = [
            char for i, char in enumerate(message_text) if (i + 1) % 3 == 0 and char in self.VOWELS
        ]
        self._current_usage += self.THIRD_VOWEL_COST * len(third_vowels)

    def _add_length_penalty(self, message_text: str):
        if len(message_text) > 100:
            self._current_usage += self.LENGTH_PENALTY

    def _add_uniqueness_bonus(self, words: List[str]):
        if len(words) == len(set(words)):
            self._current_usage -= self.UNIQUE_BONUS

    def _add_palindrome_cost(self, message_text: str):
        text_alphanumeric = "".join([char.lower() for char in message_text if char.isalnum()])
        if text_alphanumeric[::-1] == text_alphanumeric:
            self._current_usage *= 2
