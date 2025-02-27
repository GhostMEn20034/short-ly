from src.utils.error_utils import generate_error_response

__qr_code_already_exists_error_details = generate_error_response(
    location=["body", "linkShortCode"],
    message="Cannot create a QR Code",
    reason="There's already a QR code for the link with the given short code.",
    input_value="Some-Short-Code",
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
        "Creates a QR Code according to provided information. <br><br>"
        "IF you want to create a QR code for **Existing** link, "
        "you need to specify a link's short code in `linkShortCode` key.<br><br>"
        "IF you want to create a QR code + **New** link, "
        "you need to specify data required to create a link in `linkToCreate` key "
        "(see create shortened url route)."
    ),
    "responses": {
        201: {
            "description": "QR Code created successfully",
        },
        400: {
            "description": "QR Code already exists for this link",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            __qr_code_already_exists_error_details,
                        ]
                    }
                }
            },
        },
        403: {
            "description": "Only owner can create a QR Code for his links, "
                           "(If you specified that you wanna create a QR Code for existing link)",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You are not the owner of this shortened url",
                    }
                }
            },
        },
        404: {
            "description": "Server cannot find a shortened URL with the specified short code, "
                           "(If you specified that you wanna create a QR Code for existing link)",
        },
        500: {
            "description": "Server unable to generate a short code "
                           "(If you specified that you wanna create a QR Code for existing link)",
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
