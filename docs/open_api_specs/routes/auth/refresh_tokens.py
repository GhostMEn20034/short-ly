specs = {
    "description": "Refreshes both access and refresh tokens",
    "responses": {
        200: {
            "description": "Tokens are refreshed",
        },
        401: {
            "description": "Refresh token is expired",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Token expired",
                    }
                }
            },
        },
        403: {
            "description": "Server cannot validate refresh token payload",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Could not validate credentials",
                    }
                }
            },
        },
        404: {
            "description": "Server cannot find a user with id extracted from the refresh token",
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