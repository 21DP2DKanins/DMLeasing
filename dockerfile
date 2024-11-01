# Use a Python base image
FROM python:3.9-slim

# Install dependencies for Kivy
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    python3-dev \
    libgl1-mesa-dev \
    libgles2-mesa-dev \
    libsm6 \
    libxrender1 \
    libx11-6 \
    libxext6 && \
    apt-get clean

# Set a working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]