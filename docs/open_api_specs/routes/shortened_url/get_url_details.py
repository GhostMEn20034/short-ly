specs = {
    "description": (
        "Returns all information about a shortened URL."
    ),
    "responses": {
        200: {
            "description": "Shortened URL is found and successfully retrieved",
        },
        403: {
            "description": "Only owner can see his shortened URL's details",
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
