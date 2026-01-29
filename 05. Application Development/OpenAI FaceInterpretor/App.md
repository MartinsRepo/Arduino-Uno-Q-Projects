# OpenAI Facedetector and Behavior Interpretation

## Setup of the App

### How to handle different Python Version

Using **pyenv virtualenv** or **conda** is not the solution, short implementing an APP in the Arduino App Lab, we don't have the possibilty to do so. In our case, **Google Mediapipe** doesn't support Python v3.13 (in Jan 26) as we have in our Debian image.

For reasons as discussed in the chapter [Running Ollama Models](https://github.com/MartinsRepo/Arduino-Uno-Q-Projects/blob/main/01.%20GenAI%20Support/01.%20Running%20Ollama%20Models/Ollama.md) we are using **Podman** shifted to an external storage sdcard.

To bypass local dependency conflicts and the lack of MediaPipe support for Python 3.13, this project containerizes the **Face AI Service** using **Podman**. This ensures a stable **Python 3.12** environment with direct hardware access to the camera, providing a seamless AI-processing API for the Arduino Lab MicroPython script.


