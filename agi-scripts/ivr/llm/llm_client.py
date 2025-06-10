class TooManyRequests(Exception):
    """Exception to mimic rate limit errors."""
    pass

class LLMClient:
    """Simple stub client returning an echo response."""
    def get_response(self, prompt: str) -> dict:
        return {"text": f"Response: {prompt}"}
