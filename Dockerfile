FROM python:3.12-slim

# Prevent Python from writing pyc files & buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create the staticfiles directory
RUN mkdir -p /app/staticfiles

# Port 8080 is the standard for Google Cloud Run
EXPOSE 8080

# We run migration/collectstatic via the CI/CD or a wrapper,
# but for the container start, we focus on Gunicorn.
# Note: port changed to 8080
CMD ["gunicorn", "backend_api.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "3", "--timeout", "120"]