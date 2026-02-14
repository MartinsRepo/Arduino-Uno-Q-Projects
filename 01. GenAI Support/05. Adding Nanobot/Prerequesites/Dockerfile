FROM ghcr.io/arduino/app-bricks/python-apps-base:0.6.4

# Switch to root to install system deps
USER root

# Install git
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
    && rm -rf /var/lib/apt/lists/*

# Clone nanobot repository
WORKDIR /opt
RUN git clone https://github.com/MartinsRepo/nanobot.git

# Install nanobot (editable mode)
WORKDIR /opt/nanobot
RUN pip install --no-cache-dir -e .

# Switch back to default app user (IMPORTANT)
USER app

# Return to app working directory
WORKDIR /app


