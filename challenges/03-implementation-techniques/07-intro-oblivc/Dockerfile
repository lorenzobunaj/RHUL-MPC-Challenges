FROM debian:bullseye

ENV DEBIAN_FRONTEND=noninteractive

# 🛠 Install build tools and dependencies
RUN apt-get update && apt-get install -y \
    build-essential gcc g++ git wget cmake \
    libtool automake bison flex libssl-dev libffi-dev \
    libgcrypt20-dev pkg-config m4 \
    curl rsync unzip perl socat netcat \
    ocaml ocaml-base \
    ocamlbuild ocaml-findlib libnum-ocaml-dev \
    && rm -rf /var/lib/apt/lists/*

# 🧠 Clone and compile Obliv-C
RUN git clone https://github.com/samee/obliv-c.git /opt/obliv-c && \
    cd /opt/obliv-c && \
    ./configure && \
    make

# 🩹 Patch obliv.h to declare revealOblivInt
RUN sed -i '/typedef oblivBit obliv int;/a void revealOblivInt(int* dest, obliv int* src, int party);' /opt/obliv-c/src/ext/oblivc/obliv.h

# ➕ Patch obliv.c to define revealOblivInt
RUN echo 'void revealOblivInt(int* dest, obliv int* src, int party) { __obliv_c__reveal_bits(dest, src, 1, party); }' >> /opt/obliv-c/src/ext/oblivc/obliv.c

# 🔁 Rebuild Obliv-C after patch
RUN cd /opt/obliv-c && make clean && make

# 📁 Prepare challenge workspace
RUN mkdir /challenge
WORKDIR /challenge

# 📦 Copy source files into container
COPY files/ ./files/
COPY run.sh .
COPY flag.txt .

# 🧱 Compile the program using patched oblivcc
RUN /opt/obliv-c/bin/oblivcc -O2 ./files/main.c -o main && chmod +x run.sh

# 👤 Switch to non-root user
RUN useradd -m ctfuser && chown -R ctfuser /challenge
USER ctfuser

# 🚪 Expose port for testing, if needed
EXPOSE 1337

# ▶️ Run script (optional)
CMD ["./run.sh"]