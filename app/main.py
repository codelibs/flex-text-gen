import logging
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import RootModel
from string import Template

from app.config import load_config
from app.llm import generate_text

# Configure logging for the application
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

# Load configuration once at module level (if static)
app_config = load_config("config.yaml")
logger.info(f"Ollama URL: {app_config.ollama.url}")


app = FastAPI()


# Use RootModel to accept any JSON structure
class RequestData(RootModel[dict]):
    pass


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "data": exc.detail.get("data", "An error occurred") if isinstance(exc.detail, dict) else "An error occurred",
            "duration": exc.detail.get("duration", 0) if isinstance(exc.detail, dict) else 0,
        }
    )


@app.post("/generate")
async def generate(request_data: RequestData, request: Request):
    data = request_data.root  # Access the underlying dictionary
    logger.info(f"Received request data: {data}")

    start_time = time.time()

    # Retrieve system instruction and prompt templates from configuration
    system_instruction_template = Template(app_config.system_instruction)
    prompt_template = Template(app_config.prompt)

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
        output = generate_text(app_config.ollama, messages)
    except Exception as e:
        logger.exception("Error during text generation:")
        raise HTTPException(status_code=500, detail={
            "data": str(e),
            "duration": time.time() - start_time,
        })

    return {
        "status": "success",
        "data": output,
        "duration": time.time() - start_time,
    }


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Uvicorn server on port 8000...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, workers=1, reload=False)
