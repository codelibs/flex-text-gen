from dataclasses import dataclass
from typing import Any, Dict
import yaml

DEFAULT_OLLAMA_URL = "http://ollama:11434"
DEFAULT_OLLAMA_MODEL = "phi4"

@dataclass
class OllamaConfig:
    url: str
    model: str
    options: Dict[str, Any]

@dataclass
class AppConfig:
    ollama: OllamaConfig
    system_instruction: str
    prompt: str

def load_config(config_path: str = "config.yaml") -> AppConfig:
    """
    Load the application configuration from a YAML file.

    Args:
        config_path (str): The path to the configuration YAML file.

    Returns:
        AppConfig: The application configuration object.
    """
    with open(config_path, "r", encoding="utf-8") as f:
        data: Dict[str, Any] = yaml.safe_load(f)

    ollama_options = data.get("ollama", {}).get("options", {})
    ollama_data = data.get("ollama", {})

    ollama_config = OllamaConfig(
        url=ollama_data.get("url", DEFAULT_OLLAMA_URL),
        model=ollama_data.get("model", DEFAULT_OLLAMA_MODEL),
        options=ollama_options
    )
    
    app_config = AppConfig(
        ollama=ollama_config,
        system_instruction=data.get("system_instruction", ""),
        prompt=data.get("prompt", "")
    )
    
    return app_config