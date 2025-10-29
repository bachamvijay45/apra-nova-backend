FROM python:3.11-bookworm

RUN apt-get update && apt-get install -y \
    net-tools \
    iproute2 \
    iputils-ping \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*


# Set workdir
WORKDIR /app

# Prevent Python bytecode and buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn psycopg2-binary

# Copy Django project
COPY . .

# Expose port
EXPOSE 8000

# Default command (will be overridden by docker-compose)
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
