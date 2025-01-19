from openai import OpenAI

def validate_api_key(api_key: str) -> bool:
    """
    Validate the provided OpenAI API key by making a test request.
    """
    try:
        client = OpenAI(api_key = api_key)  # Set the API key
        # Make a simple API request to validate the key
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say this is a test",
                }
            ],
            model="gpt-4o",
        )
        return True
    except chat_completion.AuthenticationError:
        # Handle invalid API key
        print("Invalid API key.")
        return False
    except chat_completion.OpenAIError as e:
        # Handle other OpenAI-specific errors
        print(f"OpenAI error: {e}")
        return False
    except Exception as e:
        # Log any unexpected errors
        print(f"Unexpected error: {e}")
        return False
