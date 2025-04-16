FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables for development
ENV PYTHONUNBUFFERED=1
ENV FLASK_DEBUG=1
ENV FLASK_ENV=development
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 5000

# Use dev.py for hot reloading
CMD ["python", "app.py"] 