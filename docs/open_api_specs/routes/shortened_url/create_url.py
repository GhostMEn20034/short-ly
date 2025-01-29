from src.utils.error_utils import generate_error_response

__short_code_already_exists_error_details = generate_error_response(
    location=["body", "short_code"],
    message="Unable to create a shortened url",
    reason="Entered short code already exists",
    input_value="twitch-tv",
    error_type="domain_error"
)

__unable_to_generate_short_code_error_details = generate_error_response(
    location=["body", "short_code"],
    message="Unable to generate short code",
    reason="Currently, server cannot generate short code",
    input_value="",
    error_type="internal_error"
)

specs = {
    "description": (
        "Creates Shortened URL according to provided information. <br><br>"
        'IF you want to use GENERATED SHORT CODE, '
        '`is_short_code_custom` must be `false`'),
    "responses": {
        201: {
            "description": "Shortened URL created successfully",
        },
        400: {
            "description": "Short code already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            __short_code_already_exists_error_details,
                        ]
                    }
                }
            },
        },
        500: {
            "description": "Server unable to generate a short code",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            __unable_to_generate_short_code_error_details,
                        ]
                    }
                }
            },
        }
    }
}
