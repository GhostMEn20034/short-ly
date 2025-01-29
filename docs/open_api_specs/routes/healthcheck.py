specs = {
    "description": "Route to check if server is up",
    "responses": {
        200: {
            "description": "server is alive",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ok",
                    }
                }
            },
        },
    }
}
