FROM python:3.10

WORKDIR /app

# Install system dependencies with retries
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with multiple retries and timeout
RUN pip install --no-cache-dir --retries 10 --default-timeout=1000 -r requirements.txt

# Copy the rest of the application
COPY . .

EXPOSE 7860

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
