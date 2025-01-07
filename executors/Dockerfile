FROM ubuntu:22.04 as base

# Copy shared functions script and set permissions
COPY shared-functions.sh /shared-functions.sh
RUN chmod +x /shared-functions.sh

# Dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libcap-dev \
    libsystemd-dev \
    libseccomp-dev \
    git \
    pkg-config \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/ioi/isolate.git \
    && cd isolate \
    && make isolate \
    && cp isolate /bin/isolate \
    && cd .. \
    && rm -rf isolate
# unpriviliged user creation
RUN useradd -m -u 1000 executor