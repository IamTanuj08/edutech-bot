FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY backend/app /app/app
COPY backend/scripts /app/scripts
COPY data /app/data
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["sh","-c","python scripts/ingest.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
