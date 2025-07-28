# Dockerfile (for PLUTO-JACKAL API service)
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Expose the port (will be overridden by $PORT in cloud)
EXPOSE 8000

# Run the application
# Use $PORT environment variable injected by Render/Railway
CMD ["sh", "-c", "uvicorn pluto_jackal_api:app --host 0.0.0.0 --port ${PORT:-8000}"]
