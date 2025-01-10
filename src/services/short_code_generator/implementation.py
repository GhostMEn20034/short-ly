import random
import string

from .abstract import AbstractShortCodeGenerator
from src.core.exceptions.shortened_url import MaxRetriesExceeded


class ShortCodeGenerator(AbstractShortCodeGenerator):
    @staticmethod
    def _generate_random_string(code_length: int) -> str:
        """
        Generates a random string of given length.
        """
        s = string.ascii_lowercase + string.digits
        return ''.join(random.sample(s, code_length))

    def generate_short_code(self, code_length: int, max_retries: int) -> str:
        """
        Generates short codes iteratively.

        Yields short codes up to max_retries.
        Raises MaxRetriesExceeded if retries are exhausted.

        if your code is unique, you can break a loop with generator
        """
        for _ in range(max_retries):
            yield self._generate_random_string(code_length)

        raise MaxRetriesExceeded(max_retries)
