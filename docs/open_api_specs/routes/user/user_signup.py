from src.utils.error_utils import generate_error_response

__email_already_taken_error_details = generate_error_response(
    location=["body", "email"],
    message="Email already taken.",
    reason="The user with this email already exists",
    input_value="your@email.com",
    error_type="domain_error"
)

specs = {
    "description": "Creates user using provided data",
    "responses": {
        201: {
            "description": "User created successfully",
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