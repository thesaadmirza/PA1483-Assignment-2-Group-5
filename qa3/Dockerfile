FROM python:3.13-slim
WORKDIR /app
COPY config/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY scripts/ .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "1", "app:app"]
