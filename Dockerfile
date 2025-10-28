# File: Dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput || true

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

# Use Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "core.wsgi:application"]
