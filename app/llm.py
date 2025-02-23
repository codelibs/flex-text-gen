import logging
from transformers import pipeline
from typing import Dict, List
import torch

# Set up logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_pipeline(model_name: str):
    """
    Create and return the HuggingFace text-generation pipeline with the specified model.

    Args:
        model_name (str): The name of the model to be used.

    Returns:
        pipeline: An initialized text-generation pipeline.
    """
    # Check for CUDA first, then MPS, otherwise use CPU
    if torch.cuda.is_available():
        device = 0  # For CUDA, device index 0 is used
        dtype = "auto"  # Automatically choose the dtype
        logger.info("CUDA is available. Using CUDA for inference.")
    elif torch.backends.mps.is_available():
        device = "mps"  # For MPS, pass "mps" as the device (supported in recent Transformers versions)
        dtype = None
        logger.info("MPS device is available. Using MPS for inference.")
    else:
        device = -1  # CPU
        dtype = None
        logger.info("No CUDA or MPS device available. Using CPU for inference.")

    logger.info(f"Creating pipeline for model: {model_name} on device: {device}")
    return pipeline("text-generation", model=model_name, device=device , torch_dtype=dtype)


def generate_text(
    llm_pipeline, messages: List[Dict[str, str]], parameters: dict
) -> str:
    """
    Generate text using the provided LLM pipeline, prompt messages, and parameters.

    Args:
        llm_pipeline: An initialized HuggingFace text-generation pipeline.
        messages (List[Dict[str, str]]): List of messages containing system and user prompts.
        parameters (dict): Generation parameters (e.g., max_length, temperature).

    Returns:
        str: The generated text.
    """
    logger.info("Generating text with provided pipeline and parameters.")
    result = llm_pipeline(messages, **parameters)
    generated_text = result[0]["generated_text"]
    logger.info("Text generation complete.")
    return generated_text
