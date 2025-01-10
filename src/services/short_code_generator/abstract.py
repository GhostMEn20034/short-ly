from abc import ABC, abstractmethod


class AbstractShortCodeGenerator(ABC):

    @abstractmethod
    def generate_short_code(self, code_length: int, max_retries: int) -> str:
        pass
