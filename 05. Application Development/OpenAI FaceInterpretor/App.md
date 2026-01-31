# AI Face Behavior Detector (Arduino Lab x OpenAI)

This project implements a high-performance facial expression and behavior analysis system on an Arduino/Qualcomm development board. It uses a unique **hybrid architecture** to bypass local software limitations by bridging a MicroPython frontend with a containerized AI backend.

## 🌟 Key Features

-   **Real-time Analysis:** Detects facial muscle movements and head poses using GPT-4o-mini.

-   **Hybrid Architecture:** Combines the simplicity of Arduino Lab (MicroPython) with the power of Containerization (Podman).

-   **Edge-Filtered Vision:** Uses Google MediaPipe locally inside the container to detect faces before sending data to the cloud, saving bandwidth and API costs.

-   **Live Stream:** Includes a built-in MJPEG HTTP stream to monitor the camera feed and AI overlays via any web browser.

- **OLED SPI Display:** The LLM output is displayed in a STM driven SPI display.


## 🏗️ The Architecture: Why Podman?

Standard development on embedded boards often hits a "Dependency Wall." This project solves several critical issues:

1.  **Python Version Conflict:** Google MediaPipe currently requires **Python 3.12**. Many modern board OS builds come with Python 3.13, which is not yet supported.

2.  **Environment Isolation:** Using a Podman container ensures that heavy libraries like OpenCV and MediaPipe do not clutter or break the host system.

3.  **Hardware Pass-through:** We explicitly map the USB camera (`/dev/video2`) into the container to ensure stable driver access.

Here is a clean, organized breakdown of your project structure. This layout helps distinguish between the **containerized backend**, the **application logic**, and the **hardware configuration**.

## 📂 Project Architecture

### 🐳 Docker (Intelligence Layer)

This directory houses the containerized backend where the heavy lifting happens.

-   [**Dockerfile**](./source/Dockerfile): Defines the environment. It sets up **Python 3.12** and installs system-level dependencies like `ffmpeg` (for video processing) and `v4l-utils` (for camera handling).

-   [**face_service.py**](./source/face_service.py): The "Intelligence Core." A Flask-based API that integrates **MediaPipe** for vision and **OpenAI** for logic/processing.

-   [**requirement.txt**](./source/requirement.txt): Lists all necessary Python libraries (Flask, mediapipe, openai, etc.).


### 🐍 Python (Bridge Layer)

-   [**main.py**](./source/main.py): A MicroPython script designed for **Arduino Lab**. It acts as the UI or the communication bridge between your hardware and the Dockerized service.


### 🔌 Sketch (Hardware Layer)

-   [**sketch.ino**](./source/sketch.ino): The C++ source code for the low-level hardware configuration (GPIO pins, sensor polling, etc.).

-   **`sketch.yaml`**: Metadata for the Arduino project, ensuring the IDE and CLI know how to compile and upload the code.


### 🔑 Configuration

-   [**env**](./source/env): A protected file containing your **OpenAI API Key**. _Note: Never commit this file to public version control (like GitHub)._

## 🚀 Start the Project

### Podman Build in an Arduino Shell

    TMPDIR=/mnt/sd podman build --network host -t face-ai-service .

### Save the Podman Image on SD

    TMPDIR=/mnt/sd/podman_temp_space podman save face-ai-service:latest -o /mnt/sd/face_ai.tar

### Open an Arduino Root Shell

    sudo -i

### Copy the Image from Arduino User

    TMPDIR=/mnt/sd/podman_temp_space  podman load -i /mnt/sd/face_ai.tar

### Start the Container

    podman run --rm -d   --name face-ai   --privileged   --security-opt label=disable   --device-cgroup-rule='c 81:* rmw'   --network host   --device /dev/video2   --device /dev/video3   --device /dev/media0   -e PYTHONUNBUFFERED=1   localhost/face-ai-service:latest

### and Run the App

### Open a Browser Window on the Host PC

    http://<host pc ip>:5000/video_feed


## How to handle different Python Version

Using **pyenv virtualenv** or **conda** is not the solution, short implementing an APP in the Arduino App Lab, we don't have the possibilty to do so. In our case, **Google Mediapipe** doesn't support Python v3.13 (in Jan 26) as we have in our Debian image.

For reasons as discussed in the chapter [Running Ollama Models](https://github.com/MartinsRepo/Arduino-Uno-Q-Projects/blob/main/01.%20GenAI%20Support/01.%20Running%20Ollama%20Models/Ollama.md) we are using **Podman** shifted to an external storage sdcard.

To bypass local dependency conflicts and the lack of MediaPipe support for Python 3.13, this project containerizes the **Face AI Service** using **Podman**. This ensures a stable **Python 3.12** environment with direct hardware access to the camera, providing a seamless AI-processing API for the Arduino Lab MicroPython script.

> Written with [StackEdit](https://stackedit.io/).
