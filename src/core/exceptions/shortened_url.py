class MaxRetriesExceeded(Exception):
    def __init__(self, max_retries: int):
        super().__init__(f"Maximum number of retries exceeded: {max_retries}.")
