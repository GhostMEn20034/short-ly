def generate_error_response(
    location: list,
    message: str,
    reason: str,
    input_value: str = "",
    error_type: str = "value_error",
) -> dict:
    return {
        "type": error_type,
        "loc": location,
        "msg": message,
        "input": input_value,
        "ctx": {
            "reason": reason
        }
    }