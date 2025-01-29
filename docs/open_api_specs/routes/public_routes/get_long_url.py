specs = {
    "description": "Redirects to original URL by specified short code",
    "responses": {
        307: {
            "description": "Redirect to the original URL",
            "headers": {
                "X-Cache-Status": {
                    "description": "Cache status of the retrieved URL, "
                                   "HIT if URL is retrieved from cache, MISS if URL is retrieved from primary storage",
                    "schema": {
                        "type": "string",
                        "enum": ["HIT", "MISS"],  # List of possible values
                        "example": "HIT",  # Default example shown
                    },
                }
            },
        },
        404: {
            "description": "Short URL not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "short_code": "Url with short code twitch-tv doesn't exist"
                        }
                    }
                }
            },
        },
    }
}
