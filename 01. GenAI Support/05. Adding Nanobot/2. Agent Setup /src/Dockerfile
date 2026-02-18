FROM ghcr.io/arduino/app-bricks/python-apps-base:0.6.4

USER root

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Optional tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends mc && \
    rm -rf /var/lib/apt/lists/*

USER arduino
WORKDIR /app
