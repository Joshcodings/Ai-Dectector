# Use a lightweight python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOME=/home/user

# Create non-root user for Hugging Face security compatibility
RUN useradd -m -u 1000 user
WORKDIR $HOME/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY --chown=user:user backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application files with correct ownership
COPY --chown=user:user backend/ ./backend/
COPY --chown=user:user frontend/ ./frontend/
COPY --chown=user:user best_model.keras .
COPY --chown=user:user .gitignore .

# Hugging Face Spaces routes traffic to port 7860
EXPOSE 7860

# Switch to the non-root user
USER user

# Set working directory to backend folder to run the server
WORKDIR $HOME/app/backend

# Command to run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
