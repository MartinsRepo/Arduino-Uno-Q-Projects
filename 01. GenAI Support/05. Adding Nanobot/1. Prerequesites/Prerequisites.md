
# Prequisits

Using **Arduino App Lab**, it uses a **predefined base image** (`python-apps-base:0.6.4`) and generates containers dynamically. 

## What App Lab Actually Does

When you press **Run**:

-   It does **NOT** build a Dockerfile from your project.
    
-   It starts a container from  
    `ghcr.io/arduino/app-bricks/python-apps-base:0.6.4`
    
-   It mounts your project into the container.
    
-   It runs `/run.sh`.
    
So our project is executed **inside a prebuilt image**.

### What we can't do
You cannot directly modify:

-   the Dockerfile
    
-   the base image layers
    
-   installed apt packages

## How to run Nanobot

We extend the original image with the **nanobot**.

## Create Your Own Derived Image

#### Step 1: Create your own Dockerfile

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


#### Step 2: Build it

    docker build --build-arg OPENAI_API_KEY=sk-xxxx -t my-python-apps-base:0.6.4 .
#### Step 3: Tag it as the official image

    docker tag my-python-apps-base:0.6.4 ghcr.io/arduino/app-bricks/python-apps-base:0.6.4

