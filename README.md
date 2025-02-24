# FlexTextGen

FlexTextGen is a general API server that leverages Ollama's text-generation service.  
Built with FastAPI and Uvicorn, it allows flexible configuration through a YAML file (`config.yaml`), where you can specify system instructions, prompt templates, the Ollama endpoint URL, model name, and generation options (e.g., temperature, top_p, max_tokens).

FlexTextGen is designed to work in tandem with an Ollama container. Use docker compose to orchestrate both services.

## Key Features

- **Flexible Configuration**  
  Define system instructions, prompt templates, Ollama API settings, and generation parameters in `config.yaml`.

- **Placeholder Substitution**  
  Safely substitutes placeholders (e.g., `${word}`) in your prompts using values from incoming JSON requests.

- **Docker Support**  
  Easily build and run the application in Docker. A sample `compose.yaml` is provided to run FlexTextGen alongside an Ollama container.

## Configuration

Update your `config.yaml` to specify the Ollama API endpoint, model, and options. For example:

```yaml
ollama:
  url: "http://ollama:11434"
  model: "default-model"
  options:
    temperature: 0.7
    top_p: 0.9
    max_tokens: 256
system_instruction: |
  You are an advanced language model that explains words in detail.
prompt: "Explain the word '${word}' in detail."

## Docker Setup

### Building the Image

FlexTextGen is designed to run with Ollama, while Ollama runs in a separate container.
For a standard build (using apt-installed Python 3.13):

```sh
docker compose build
```

### Running with Docker Compose

A sample compose.yaml is provided to run FlexTextGen together with an Ollama container.
For example:

```
version: "3.8"
services:
  flex-text-gen:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - ollama

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ${HOME}/.ollama:/root/.ollama
```

To start both services, run:

```sh
docker compose up
```

## API Usage

FlexTextGen exposes a /generate endpoint that accepts JSON requests. For example, to get an explanation of a word:

```
{
  "word": "Java"
}
```

The server will substitute the placeholder in the prompt template and send a request to the Ollama API. The generated result is then returned in the response.

## Logging and Debugging

Logging is enabled to help trace server operations and API calls. Check the container logs for detailed information.
