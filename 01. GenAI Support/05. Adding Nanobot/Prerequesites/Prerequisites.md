
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
For storage purpose, we created a **Podman-Image**, as shown in projects below.
Using **App Lab** projects together with Podman applications, we have to install Podman in the prebuild image and run the container in `--privileged` mode.

## Create Your Own Derived Image

#### Step 1: Create your own Dockerfile

    FROM ghcr.io/arduino/app-bricks/python-apps-base:0.6.4
    RUN apt-get update && \
    apt-get install -y \
        podman \
    && rm -rf /var/lib/apt/lists/*

#### Step 2: Build it

    docker build -t my-python-apps-base:0.6.4 .

#### Step 3: Tag it as the official image

    docker tag my-python-apps-base:0.6.4 ghcr.io/arduino/app-bricks/python-apps-base:0.6.4

