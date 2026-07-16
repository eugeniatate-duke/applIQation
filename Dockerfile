FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend backend
COPY src src
COPY models models
RUN ls -lah /app/models/distilbert && \
  test -f /app/models/distilbert/model.safetensors
COPY data data
COPY setup.py .

ENV PYTHONPATH=/app

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
