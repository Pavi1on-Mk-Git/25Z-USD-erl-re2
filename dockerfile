FROM debian:bookworm-slim

WORKDIR /usd

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       bash \
       curl \
       ca-certificates \
       build-essential \
       libosmesa6-dev \
       patchelf \
       libglib2.0-0 \
       libglew-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://pdm-project.org/install.sh | bash -s -- -v 2.26.3

RUN mkdir -p /root/.mujoco

RUN curl -L https://github.com/google-deepmind/mujoco/releases/download/2.1.0/mujoco210-linux-x86_64.tar.gz | \
    tar xz -C /root/.mujoco/

ENV PATH="/root/.local/bin:$PATH"

ENV LD_LIBRARY_PATH="/root/.mujoco/mujoco210/bin:"

ENV MUJOCO_GL=osmesa

COPY . .

RUN pdm install
