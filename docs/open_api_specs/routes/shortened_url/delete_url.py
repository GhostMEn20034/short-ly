specs = {
    "description": (
        "Deletes shortened URL by specified short code"
    ),
    "responses": {
        204: {
            "description": "Shortened URL deleted successfully",
        },
        403: {
            "description": "Only owner allowed to delete his shortened URLs",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You are not the owner of this shortened url",
                    }
                }
            },
        },
        404: {
            "description": "Server cannot find a shortened URL with the specified short code",
        },
    }
}
