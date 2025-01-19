import openai


def validate_api_key(api_key: str) -> bool:
    """
    Validate the provided OpenAI API key by making a test request.
    """
    try:
        openai.api_key = api_key
        openai.Completion.create(engine="text-davinci-003", prompt="Test", max_tokens=1)
        return True
    except Exception:
        return False