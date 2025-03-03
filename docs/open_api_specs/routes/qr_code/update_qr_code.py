specs = {
    "description": (
        "Applies new data to the QR Code."
    ),
    "responses": {
        200: {
            "description": "QR Code updated successfully",
        },
        403: {
            "description": "Only owner allowed to update his QR Codes",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You are not the owner of this QR Code",
                    }
                }
            },
        },
        404: {
            "description": "Server cannot find a QR Code to update",
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "examples": {
                        "Some field is invalid": {
                            "summary": "All fields must satisfy specified conditions",
                            "value": {
                                "detail": [
                                    {
                                        "loc": [
                                            "body",
                                            "someField"
                                        ],
                                        "msg": "SomeError",
                                        "type": "validation_error"
                                    }
                                ]
                            }
                        },
                        "Wrong request body at all": {
                            "summary": "Request body don't have required fields at all",
                            "value": {
                                "detail": "Invalid request body",
                            },
                        },
                    }
                }
            },
        },
    }
}
