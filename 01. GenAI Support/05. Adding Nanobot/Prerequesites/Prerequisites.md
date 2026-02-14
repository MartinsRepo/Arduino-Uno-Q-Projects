
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

We extend the original image with the **nanon bot**.

## Create Your Own Derived Image

#### Step 1: Create your own Dockerfile

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
    
    # switch back to original user (important!)
    USER app


#### Step 2: Build it

    docker build -t my-python-apps-base:0.6.4 .

#### Step 3: Tag it as the official image

    docker tag my-python-apps-base:0.6.4 ghcr.io/arduino/app-bricks/python-apps-base:0.6.4

