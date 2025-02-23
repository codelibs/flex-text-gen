import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import RootModel
from string import Template
from contextlib import asynccontextmanager

from app.config import load_config
from app.llm import create_pipeline, generate_text

# Configure logging for the application
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("flex-text-gen")

# Load configuration once at module level (if static)
config = load_config("config.yaml")
generation_parameters = config.get("parameters", {})
model_name = config.get("model", "microsoft/phi-4")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading LLM pipeline...")
    # Load the model only once at startup and store it in app.state
    app.state.llm_pipeline = create_pipeline(model_name)
    logger.info("LLM pipeline loaded successfully.")
    yield
    # Optionally, add any shutdown cleanup here
    logger.info("Shutting down...")


app = FastAPI(lifespan=lifespan)


# Use RootModel to accept any JSON structure
class RequestData(RootModel[dict]):
    pass


@app.post("/generate")
async def generate(request_data: RequestData, request: Request):
    data = request_data.root  # Access the underlying dictionary
    logger.info(f"Received request data: {data}")

    # Retrieve system instruction and prompt templates from configuration
    system_instruction_template = Template(config.get("system_instruction", ""))
    prompt_template = Template(config.get("prompt", ""))

    # Safely substitute placeholders in the templates with values from the request data
    system_instruction = system_instruction_template.safe_substitute(data)
    prompt = prompt_template.safe_substitute(data)

    logger.info(f"System instruction: {system_instruction}")
    logger.info(f"Prompt: {prompt}")

    # Prepare the messages for the LLM
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": prompt},
    ]

    try:
        # Retrieve the model pipeline from app.state instead of creating it again
        output = generate_text(app.state.llm_pipeline, messages, generation_parameters)
    except Exception as e:
        logger.exception("Error during text generation:")
        raise HTTPException(status_code=500, detail=str(e))

    logger.info("Text generation successful.")
    return {"result": output}


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Uvicorn server on port 8000...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, workers=1, reload=False)
