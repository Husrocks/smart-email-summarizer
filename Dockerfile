# Use an official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to access models/ and backend/
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

# Expose the port Hugging Face uses
EXPOSE 7860

# Run the application
# We use 0.0.0.0 to make it accessible externally
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
