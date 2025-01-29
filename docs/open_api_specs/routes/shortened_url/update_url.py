specs = {
    "description": (
        "Apply new data to shortened URL."
    ),
    "responses": {
        200: {
            "description": "Shortened URL updated successfully",
        },
        403: {
            "description": "Only owner allowed to update his shortened URLs",
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
