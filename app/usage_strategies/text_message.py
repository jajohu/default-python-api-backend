import re
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

    def calculate_usage(self) -> float:
        text = self._message.text
        cost = self.BASE_COST

        chars = len(text.replace(" ", ""))
        cost += (self.CHAR_COST * chars)

        words = text.split(" ")
        for word in words:
            if 1 <= len(word) <= 3: cost += self.LENGTH_1_3
            elif 4 <= len(word) <= 7: cost += self.LENGTH_4_7
            elif len(words) >= 8: cost += self.LENGTH_8_PLUS

        third_vowels = [char for i, char in enumerate(text) if (i + 1) % 3 == 0 and char in self.VOWELS]
        cost += self.THIRD_VOWEL_COST * len(third_vowels)

        if len(text) > 100: cost += self.LENGTH_PENALTY

        if len(words) == len(set(words)): cost -= self.UNIQUE_BONUS

        text_alphanumeric = "".join([char.lower() for char in text if char.isalnum()])
        if text_alphanumeric[::-1] == text_alphanumeric: cost *= 2

        return max(self.BASE_COST, cost)
        