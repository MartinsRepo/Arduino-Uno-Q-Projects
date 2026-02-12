FROM ghcr.io/arduino/app-bricks/python-apps-base:0.6.4

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        podman \
    && rm -rf /var/lib/apt/lists/*

# switch back to original user (important!)
USER app

