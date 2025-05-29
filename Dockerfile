# Use official Python slim image for a lightweight base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies for speech recognition and audio
RUN apt-get update && apt-get install -y \
    libportaudio2 \
    libasound-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Start FastAPI and Streamlit in parallel
CMD ["sh", "-c", "uvicorn orchestrator.main:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0"]