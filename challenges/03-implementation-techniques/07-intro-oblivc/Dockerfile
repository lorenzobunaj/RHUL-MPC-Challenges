FROM debian:bullseye

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /challenge

# challenge files
COPY files/ ./files/
COPY run.sh .
COPY flag.txt .

# dependencies
RUN apt-get update && apt-get install -y \
    build-essential gcc g++ git wget cmake\
    libtool automake bison flex libssl-dev libffi-dev \
    libgcrypt20-dev pkg-config m4 \
    curl rsync unzip perl socat netcat \
    ocaml ocaml-base \
    ocamlbuild ocaml-findlib libnum-ocaml-dev \
    && rm -rf /var/lib/apt/lists/*

# clone and compile oblivc
RUN git clone https://github.com/samee/obliv-c.git /opt/obliv-c && \
    cd /opt/obliv-c && \
    ./configure && \
    make

# path obliv.h
RUN sed -i '/typedef oblivBit obliv int;/a void revealOblivInt(int* dest, obliv int* src, int party);' /opt/obliv-c/src/ext/oblivc/obliv.h
RUN sed -i '/typedef oblivBit obliv int;/a void feedOblivInt(obliv int* dest, int party, int value);' /opt/obliv-c/src/ext/oblivc/obliv.h

# patch obliv.c
RUN echo 'void revealOblivInt(int* dest, obliv int* src, int party) { __obliv_c__reveal_bits(dest, src, 1, party); }' >> /opt/obliv-c/src/ext/oblivc/obliv.c
RUN echo 'void feedOblivInt(obliv int* dest, int party, int value) { __obliv_c__feedOblivInputs(dest, &value, 1, party); }' >> /opt/obliv-c/src/ext/oblivc/obliv.c

# rebuild oblivc
RUN cd /opt/obliv-c && make clean && make

# compile the program using patched oblivcc
RUN /opt/obliv-c/bin/oblivcc -O2 ./files/main.c -o main

# file permissions
RUN chmod +x run.sh

# non-root user for runtime
RUN useradd -m ctfuser && chown -R ctfuser /challenge
USER ctfuser

# health check (requires netcat inside container)
# HEALTHCHECK CMD nc -z localhost 1337 || exit 1

EXPOSE 1337

CMD ["./run.sh"]