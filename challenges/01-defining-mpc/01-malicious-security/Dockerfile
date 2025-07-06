FROM python:3.12-slim

WORKDIR /challenge

# challenge files
COPY files/ ./files/
COPY run.sh .
COPY flag.txt .

# dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    libffi-dev \
    libssl-dev \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pwntools
RUN pip install --no-cache-dir pycryptodome

# file permissions
RUN chmod +x run.sh

# EXPOSE 1337

CMD ["./run.sh"]