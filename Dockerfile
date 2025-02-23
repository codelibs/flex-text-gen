# Use Python 3.13 slim as the base image
FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . .

# Copy the entrypoint script and set executable permission
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port 8000
EXPOSE 8000

# Use the entrypoint script to start uvicorn with workers from env variable
CMD ["/app/entrypoint.sh"]