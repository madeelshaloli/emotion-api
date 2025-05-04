# Use official Python image
FROM python:3.10-slim

# Install system dependencies needed for DeepFace and OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy your project files into the container
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 (used by Flask)
EXPOSE 5000

# Run your app
CMD ["python", "app.py"]
