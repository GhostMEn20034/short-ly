specs = {
    "description": (
        "Returns all information about a QR Code."
    ),
    "responses": {
        200: {
            "description": "QR Code is found and successfully retrieved",
        },
        403: {
            "description": "Only owner can see his QR Code's details",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You are not the owner of this QR Code",
                    }
                }
            },
        },
        404: {
            "description": "Server cannot find a QR code with the specified id",
        },
    }
}
