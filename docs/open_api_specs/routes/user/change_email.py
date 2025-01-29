from src.utils.error_utils import generate_error_response

__email_already_taken_error_details = generate_error_response(
    location=["body", "email"],
    message="Email already taken.",
    reason="The user with this email already exists",
    input_value="your@new-email.com",
    error_type="domain_error"
)

specs = {
    "description": "Update user's email address if it's not already taken.",
    "responses": {
        200: {
            "description": "User's email address successfully changed",
        },
        400: {
            "description": "Email already taken",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            __email_already_taken_error_details,
                        ]
                    }
                }
            },
        },
    }
}
