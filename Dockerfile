# Super simple Docker setup - no VM needed
FROM python:3.12-slim

WORKDIR /app

# Install minimal OS tools (simulates Linux environment)
RUN apt-get update && apt-get install -y \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copy your code
COPY . /app

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

# Default: run tests
CMD ["pytest", "tests/", "-v"]


