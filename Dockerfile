FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --retries 5 -r requirements.txt

# Copy the rest of the application
COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
