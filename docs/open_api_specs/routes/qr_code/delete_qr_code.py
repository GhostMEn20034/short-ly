specs = {
    "description": (
        "Deletes the QR Code"
    ),
    "responses": {
        204: {
            "description": "QR Code deleted successfully",
        },
        403: {
            "description": "Only the owner allowed to delete his QR Codes",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You are not the owner of this QR Code",
                    }
                }
            },
        },
        404: {
            "description": "Server cannot find a QR Code to delete",
        },
    }
}
