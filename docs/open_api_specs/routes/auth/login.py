from src.utils.error_utils import generate_error_response

__wrong_password_error_details = generate_error_response(
    location=["body", "password"],
    message="Incorrect email or password",
    reason="Incorrect email or password",
    input_value="your-pwd",
    error_type="domain_error"
)

__wrong_email_error_details = generate_error_response(
    location=["body", "email"],
    message="Incorrect email or password",
    reason="Incorrect email or password",
    input_value="your@email.com",
    error_type="domain_error"
)

specs = {
    "description": "Provided user credentials",
    "responses": {
        200: {
            "description": "User logged in successfully",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "your_access_token",
                        "refresh_token": "your_refresh_token",
                    }
                }
            }
        },
        400: {
            "description": "Wrong email or password",
            "content": {
                "application/json": {
                    "examples": {
                        "wrong_password": {
                            "summary": "Incorrect password",
                            "description": "The provided password is incorrect.",
                            "value": {
                                "detail": [__wrong_password_error_details]
                            }
                        },
                        "wrong_email": {
                            "summary": "Incorrect email",
                            "description": "The provided email does not match any user account.",
                            "value": {
                                "detail": [__wrong_email_error_details]
                            }
                        }
                    }
                }
            },
        },
    }
}
