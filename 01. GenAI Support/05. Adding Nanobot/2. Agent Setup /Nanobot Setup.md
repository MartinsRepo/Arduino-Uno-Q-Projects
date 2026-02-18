# Nanobot: Arduino Uno Q Agent Bridge

## 1. Demonstration Purpose

The primary goal of this project is to demonstrate the integration of **low-power hardware (Arduino Uno Q)** with **high-level AI Agent logic**.

By using the `AgentLoop` framework, the Uno Q acts as a physical gateway for human-to-AI interaction. This setup tests:

-   **Serial-to-Agent Bridging:** The ability of the microcontroller to pass natural language prompts to a host system.
    
-   **Provider Agnosticism:** Using LiteLLM to seamlessly switch between providers (OpenAI, Anthropic, etc.) based on hardware constraints or task requirements.
    
-   **Real-time Latency:** Measuring the round-trip time from an Arduino `Serial` prompt (e.g., "What is the weather?") to a processed LLM response.
    

## 2. Project Setup

### How to install Python Libraries
As you can't use `pip install -r requirements.txt` , as usual, we have to import and install the libraries in **app.yaml**. This works not straight forward in the Arduino App Lab, so for modification **close it** and open an Arduino Shell:
In the folder ArduinoApps go into the root of your project and edit **app.yaml**

    cd ~/ArduinoApps/unoq-nanobot
    nano app.yaml` 
    
In the section **python_packages**, you can add the libraries:

> #app.yaml: The main configuration file for your Arduino App.
> #This file describes the application's metadata and properties.
> #The user-visible name of the application.
> name: unoq-nanobot
> 
> #A brief description of what the application does.
> description: ""
> 
> #The icon for the application, can be an emoji or a short string.
> icon: 😀
> 
> #This section tells the Uno Q which libraries to install via pip/package manager
> python_packages:
> - requests
> - numpy
> - litellm
> - pydantic
> - openai
> 
> #A list of network ports that the application exposes. 
> #Example: [80, 443]
> ports: []
> 
> #A list of bricks used by this application.
> bricks: []

### AI Provider Layer

-   **LiteLLM:** Acts as a universal adapter.
    
-   **Configuration:** A `config.json` file stores API keys and default model parameters (e.g., GPT-4o-mini) to ensure the agent remains configurable without code changes.
    

----------

## 3. Key Modifications

### `main.py` (Provider Initialization Fix)

Previously, the system suffered from an authentication error because the `LiteLLMProvider` was receiving the model name as its first positional argument, causing it to treat the model name as the API Key.

**Changes included:**

-   **Dynamic Config Loading:** Implemented `json.load()` to pull the `apiKey` and `model` directly from the Nanobot `config.json`.
    
-   **Keyword Argument Enforcement:** Refactored the provider instantiation to use explicit keyword arguments:
    
    Python
    
    ```
    provider = LiteLLMProvider(
        api_key=openai_key, 
        default_model=target_model
    )
    
    ```
    
-   **Error Handling:** Added robust `try-except` blocks to catch configuration mismatches before the `AgentLoop` starts.
    

### `sketch.ino` (Communication Protocol)

The sketch was optimized to handle the asynchronous nature of LLM responses.

**Changes included:**

-   **Prompt Handling:** Modified the serial buffer logic to ensure complete strings are sent to the Python bridge.
    
-   **Status Signaling:** Added LED or Serial feedback to indicate when the Agent is "thinking" versus when the system is idle.
    
-   **Reset Logic:** Improved the handshake protocol to ensure the Arduino and Python script synchronize correctly upon startup.
