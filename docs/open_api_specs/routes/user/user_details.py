specs = {
    "description": "Returns user's information",
    "responses": {
        200: {
            "description": "User's information retrieved successfully",
        },
        401: {
            "description": "Token is expired",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Token expired",
                    }
                }
            },
        },
        403: {
            "description": "Server cannot validate token payload",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Could not validate credentials",
                    }
                }
            },
        },
        404: {
            "description": "Server cannot find a user with id extracted from the auth token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Could not find user",
                    }
                }
            },
        },
    }
}
