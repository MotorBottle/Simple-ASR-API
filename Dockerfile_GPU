# Base image with PyTorch, CUDA 12.4, and cuDNN 9
FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime

# Set working directory
WORKDIR /app

# Copy only the necessary application files
COPY asr_http_server.py /app/
COPY trans_utils.py /app/

# Install required Python dependencies
RUN pip install --no-cache-dir Flask funasr librosa

# Expose the Flask service port
EXPOSE 7869

# Command to run the Flask application
CMD ["python", "asr_http_server.py"]