Here’s a draft for the `README.md` file based on your project:

---

# ASRAPI: Simple ASR API Deployment Example

This repository demonstrates a simple example of deploying the **[FunASR](https://github.com/modelscope/FunASR)** library for non-realtime automatic speech recognition (ASR). It supports processing **audio files only** and provides examples for both local Python reference and REST API deployment.

---

## Repository Contents

### Core Files:
- **`asr_http_server.py`**: Implements the REST API server for ASR transcription.
- **`trans_utils.py`**: Utility functions used by the REST API.

### Testing and Examples:
- **`testAPI.py`**: Example client script to test the REST API functionality.
- **`SoundToTextLocal.py`**: A standalone Python implementation for local ASR transcription.
- **`test.py`**: Example of using `SoundToTextLocal` for local transcription.

### Deployment Files:
- **`Dockerfile`**: Dockerfile for building GPU-accelerated Docker images (NVIDIA GPU deployment).
- **`Dockerfile_CPU`**: Dockerfile for building Docker images for simple CPU-based deployments.

### Additional Files:
- **`requirements.txt`**: Python dependencies required for the project.
- **`requestSound.wav`**: Example audio file for testing.
- **`.gitignore`**: Standard Git ignore file for Python projects.

---

## Features

1. **REST API for ASR**:
   - Provides a REST API endpoint for audio file transcription.
   - Built using Flask.
   - Example usage: `testAPI.py`.

2. **Local Python Reference**:
   - `SoundToTextLocal.py` demonstrates a standalone ASR transcription method without the need for REST APIs.
   - Example usage: `test.py`.

3. **Docker Support**:
   - Includes Dockerfiles for both GPU and CPU deployment.
   - Simplifies deployment on servers with or without GPU support.

---

## Usage

### 1. Install Dependencies

Install the necessary Python dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run REST API Server

To start the REST API server:
```bash
python asr_http_server.py
```

The server will start on `http://127.0.0.1:7869`.

### 3. Test the REST API

Use the `testAPI.py` script to test the API:
```bash
python testAPI.py
```

Example `curl` command:
```bash
curl -X POST -F "audio=@requestSound.wav" http://127.0.0.1:7869/asr
```

### 4. Local Transcription Example

Run the local transcription example:
```bash
python test.py
```

---

## Docker Deployment

### GPU Deployment

Build and run the Docker image for NVIDIA GPU:
```bash
docker build -t asr-service-gpu:v0.1.0 .
docker run --gpus all -d -p 7869:7869 --name asr-service asr-service-gpu:v0.1.0
```

### CPU Deployment

Build and run the Docker image for CPU:
```bash
docker build -f Dockerfile_CPU -t asr-service-cpu:v0.1.0 .
docker run -d -p 7869:7869 --name asr-service asr-service-cpu:v0.1.0
```

---

## Example API Request

Send an audio file to the REST API:
```bash
curl -X POST -F "audio=@path/to/audio.wav" http://127.0.0.1:7869/asr
```

---

## Limitations

- Only supports **non-realtime** ASR transcription.
- Only supports **audio files** as input.

---

## References

- [FunASR](https://github.com/modelscope/FunASR): The ASR framework used in this project.

---

Feel free to modify it as needed!