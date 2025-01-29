from src.utils.error_utils import generate_error_response

__wrong_old_password_error_details = generate_error_response(
    location=["body", "password"],
    message="Incorrect email or password",
    reason="Incorrect email or password",
    input_value="your-pwd",
    error_type="domain_error"
)

specs = {
    "description": "Update user's password",
    "responses": {
        204: {
            "description": "User's password successfully changed",
        },
        400: {
            "description": "Wrong old password",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            __wrong_old_password_error_details,
                        ]
                    }
                }
            },
        },
    }
}
