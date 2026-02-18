FROM ghcr.io/arduino/app-bricks/python-apps-base:0.6.4

USER root

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Install git
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Clone nanobot
WORKDIR /opt
RUN git clone https://github.com/MartinsRepo/nanobot.git

# Install nanobot
WORKDIR /opt/nanobot
RUN pip install --no-cache-dir -e .

# Create nanobot config directory
RUN mkdir -p /home/app/.nanobot && \
    echo '{ \
      "providers": { \
        "default": "openai", \
        "openai": { \
          "api_key": "'"${OPENAI_API_KEY}"'" \
        } \
      } \
    }' > /home/app/.nanobot/config.json

RUN chown -R app:app /home/app/.nanobot

# Switch back to app user
USER app
WORKDIR /app



