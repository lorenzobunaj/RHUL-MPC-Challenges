FROM debian:bullseye

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /challenge

# challenge files
COPY files/ ./files/
COPY run.sh .
COPY flag.txt .

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential gcc g++ git wget cmake \
    libtool automake bison flex libssl-dev libffi-dev \
    libgcrypt20-dev pkg-config m4 curl rsync unzip perl \
    socat netcat ocaml ocaml-base ocamlbuild ocaml-findlib \
    libnum-ocaml-dev gdb && \
    rm -rf /var/lib/apt/lists/*

# Clone and build Obliv-C
RUN git clone https://github.com/samee/obliv-c.git /opt/obliv-c && \
    cd /opt/obliv-c && \
    git reset --hard && git clean -fdx && \
    ./configure && \
    make

# Compile binaries
RUN /opt/obliv-c/bin/oblivcc -g ./files/party1.c ./files/common.c -o party1 && \
    /opt/obliv-c/bin/oblivcc -g ./files/party2.c ./files/common.c -o party2

# Make entrypoint executable
RUN chmod +x run.sh

# Create user
RUN useradd -m ctfuser && chown -R ctfuser /challenge
USER ctfuser

EXPOSE 1358
CMD ["./run.sh"]