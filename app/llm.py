import requests
from app.config import OllamaConfig


def generate_text(config: OllamaConfig, messages: list) -> str:
    """
    Generates text based on the given configuration and messages.

    Args:
        config (OllamaConfig): The configuration for the text generation.
        messages (list): A list of messages to be used for generating text.

    Returns:
        str: The generated text.
    """
    response = requests.post(
        f"{config.url}/api/chat",
        json={
            "model": config.model,
            "messages": messages,
            "stream": False,
            "options": config.options,
        },
    )
    if response.status_code != 200:
        response.raise_for_status()

    result = response.json()
    return result.get("message", {}).get("content", "")