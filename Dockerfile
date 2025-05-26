FROM python:3.11-slim

WORKDIR /app

# Copy requirements.txt and install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the contents of the app folder directly into /app
COPY app/ .

# Set PYTHONPATH to include /app for module resolution
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]