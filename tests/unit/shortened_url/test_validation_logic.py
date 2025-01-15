import pytest
from pydantic import ValidationError
from src.schemes.shortened_url import CreateShortenedUrlSchema


class TestShortenedUrlValidationLogic:

    def test_create_url_with_short_name_must_not_be_reserved_word(self):
        """
        User cannot use reserved words as short code
        """
        # Reserved word to test
        reserved_word = "dashboard"

        schema_data = {
            "friendly_name": "Test",
            "is_short_code_custom": True,
            "short_code": reserved_word,
            "long_url": "https://test.com",
        }

        # Verify that the schema raises a ValidationError for reserved words
        with pytest.raises(ValidationError) as exc_info:
            CreateShortenedUrlSchema(**schema_data)

        # Assert the error message is related to the reserved word
        assert f"The short code '{reserved_word}' is reserved and cannot be used." in str(exc_info.value)
