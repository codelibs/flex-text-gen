# FlexTextGen

flex-text-gen is a general API server that utilizes HuggingFaces' LLM (default model: phi4).  
It is built with FastAPI and Uvicorn, and allows configuration of system instructions, prompt templates, the LLM model, and generation parameters (e.g., temperature, max_length) via a configuration file (`config.yaml`).  
The server can also be run as a Docker container.

## Key Features

- **Flexible Configuration**  
  Define system instructions, prompt templates, LLM model, and generation parameters in `config.yaml`.

- **Placeholder Substitution**  
  Replaces placeholders (e.g., `${name}`) in the prompt using values from JSON requests.

- **Docker Support**  
  Easily build and run the application in a Docker container using the provided Dockerfile.

## Usage

1. **Build the Docker image**

   ```sh
   docker build -t flex-text-gen:latest .
   ```

2. **Run the Docker image**

   ```sh
   docker run -p 8000:8000 -v $HOME/.cache/huggingface/hub:/root/.cache/huggingface/hub flex-text-gen:latest
   ```
