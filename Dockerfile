# Base image with PyTorch, CUDA 12.4, and cuDNN 9
FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime

# Set working directory
WORKDIR /app

# Install system dependencies (including ffmpeg and other essentials)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy only the necessary application files
COPY asr_http_server.py /app/
COPY trans_utils.py /app/

# Install required Python dependencies
RUN pip install --no-cache-dir Flask funasr librosa

# Expose the Flask service port
EXPOSE 7869

# Command to run the Flask application
CMD ["python", "asr_http_server.py"]