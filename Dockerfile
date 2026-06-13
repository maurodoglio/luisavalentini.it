FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project (including media/ if present in build context)
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create data directory for SQLite (will be mounted as persistent volume)
RUN mkdir -p /data

EXPOSE 8000

# Run migrations on startup, then start gunicorn
RUN chmod +x start.sh
CMD ["./start.sh"]
