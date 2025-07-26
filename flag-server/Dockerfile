FROM python:3.12-slim

WORKDIR /flag-server

# Copy server files
COPY server.py .
COPY run.sh .

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir flask

# File permissions
RUN chmod +x run.sh

CMD ["./run.sh"]