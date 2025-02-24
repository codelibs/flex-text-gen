# Use Python 3.13 slim as the base image
FROM python:3.13-slim

# Build-time arguments for user UID and GID (default to 1000)
ARG USER_UID=1000
ARG USER_GID=1000

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . .

# Create a new group and user with the specified UID and GID, then change ownership of /app
RUN groupadd -g ${USER_GID} appgroup && \
    useradd -u ${USER_UID} -g appgroup -m -d /app appuser && \
    chown -R appuser:appgroup /app

# Copy the entrypoint script, set executable permission, and adjust ownership
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh && chown appuser:appgroup /app/entrypoint.sh

# Switch to the new user
USER appuser

# Expose port 8000
EXPOSE 8000

# Start the application using the entrypoint script
CMD ["/app/entrypoint.sh"]