import pytest
from pydantic import ValidationError

from src.schemes.shortened_url.request_bodies.create import CreateShortenedUrlRequestBody
from src.schemes.consts import reserved_words


class TestShortenedUrlValidationLogic:

    @pytest.mark.parametrize("reserved_word", list(reserved_words))
    def test_create_url_with_short_name_must_not_be_reserved_word(self, reserved_word):
        """
        User cannot use reserved words as a short code for a shortened url.
        If the short code length is between 8 and 20, assert the reserved word error.
        Otherwise, assert length-related validation errors.
        """

        schema_data = {
            "friendly_name": "Test",
            "is_short_code_custom": True,
            "short_code": reserved_word,
            "long_url": "https://test.com",
        }

        # Verify that the schema raises a ValidationError for reserved words
        with pytest.raises(ValidationError) as exc_info:
            CreateShortenedUrlRequestBody(**schema_data)

        error_message = str(exc_info.value)

        # Check for reserved word error if the short code length is valid
        if 8 <= len(reserved_word) <= 20:
            assert f"The short code '{reserved_word}' is reserved and cannot be used." in error_message
        else:
            # Assert the error is about length
            if len(reserved_word) < 8:
                assert "String should have at least 8 characters" in error_message
            elif len(reserved_word) > 20:
                assert "String should have at most 20 characters" in error_message

    @pytest.mark.parametrize(
        "invalid_short_code",
        [
            "my/short-url",  # Contains a forward slash
            "my\\long\\url",  # Contains a backward slash
            "test.invalid",  # Contains a dot
            "invalid@short",  # Contains an @ symbol
            "space code123",  # Contains a space
            "code!12345",  # Contains an exclamation mark
            "a_b_c_d123",  # Contains an underscore
        ],
    )
    def test_short_code_with_invalid_characters(self, invalid_short_code):
        """
        Test that short codes containing invalid characters raise a ValidationError
        """
        schema_data = {
            "friendly_name": "Test",
            "is_short_code_custom": True,
            "short_code": invalid_short_code,
            "long_url": "https://test.com",
        }

        # Verify that a ValidationError is raised for invalid characters
        with pytest.raises(ValidationError) as exc_info:
            CreateShortenedUrlRequestBody(**schema_data)

        # Assert the error message mentions invalid characters
        assert "contains invalid characters" in str(exc_info.value)

    @pytest.mark.parametrize(
        "valid_short_code",
        [
            "ValidCode123",  # Mixed case letters and digits
            "code-with-dash",  # Hyphen usage
            "ShortCode123456",  # Mixed case with a valid length
        ],
    )
    def test_short_code_with_valid_characters(self, valid_short_code):
        """
        Test that short codes containing only valid characters pass validation
        """
        schema_data = {
            "friendly_name": "Test",
            "is_short_code_custom": True,
            "short_code": valid_short_code,
            "long_url": "https://test.com",
        }

        # Verify that no ValidationError is raised for valid characters
        schema = CreateShortenedUrlRequestBody(**schema_data)
        assert schema.short_code == valid_short_code

    @pytest.mark.parametrize(
        "too_short_short_code",
        [
            "short",  # 5 characters
            "small1",  # 6 characters
            "seven77",  # 7 characters
        ],
    )
    def test_short_code_too_short(self, too_short_short_code):
        """
        Test that short codes shorter than 8 characters raise a ValidationError
        """
        schema_data = {
            "friendly_name": "Test",
            "is_short_code_custom": True,
            "short_code": too_short_short_code,
            "long_url": "https://test.com",
        }

        # Verify that a ValidationError is raised for short codes that are too short
        with pytest.raises(ValidationError) as exc_info:
            CreateShortenedUrlRequestBody(**schema_data)

        # Assert the error message mentions the length constraint
        assert "String should have at least 8 characters" in str(exc_info.value)

    @pytest.mark.parametrize(
        "too_long_short_code",
        [
            "thisisaverylongshortcode123",  # 25 characters
            "toolongshortcodeover20char",  # 27 characters
        ],
    )
    def test_short_code_too_long(self, too_long_short_code):
        """
        Test that short codes longer than 20 characters raise a ValidationError
        """
        schema_data = {
            "friendly_name": "Test",
            "is_short_code_custom": True,
            "short_code": too_long_short_code,
            "long_url": "https://test.com",
        }

        # Verify that a ValidationError is raised for short codes that are too long
        with pytest.raises(ValidationError) as exc_info:
            CreateShortenedUrlRequestBody(**schema_data)

        # Assert the error message mentions the length constraint
        assert "String should have at most 20 characters" in str(exc_info.value)

    def test_short_code_without_custom_flag(self):
        """
        Test that when is_short_code_custom is False, any short code should be allowed
        """
        schema_data_valid = {
            "friendly_name": "Test",
            "is_short_code_custom": False,
            "short_code": "my-valid-code123",
            "long_url": "https://test.com",
        }

        schema_data_invalid = {
            "friendly_name": "Test",
            "is_short_code_custom": False,
            "short_code": "invalid@code!",  # Invalid characters, should be allowed
            "long_url": "https://test.com",
        }

        # This should not raise any errors, even with invalid characters or lengths.
        schema_valid = CreateShortenedUrlRequestBody(**schema_data_valid)
        assert schema_valid.short_code == "my-valid-code123"

        # No validation should be done, any short code should be accepted
        schema_invalid = CreateShortenedUrlRequestBody(**schema_data_invalid)
        assert schema_invalid.short_code == "invalid@code!"