## Customizing Ollama Models in Podman

This guide explains how to create a custom model (persona) using a `Modelfile` and integrate it into a Python-based workflow.

### 1. Prerequisites (as done before)

-   **Podman** installed and running.
    
-   **Ollama** container running (e.g., named `ollama`).
    
-   Base model pulled (e.g., `qwen3:0.6B`).
    

### 2. Create a Custom Container

The `Modelfile` acts as a blueprint for your custom model. It defines the base model, system instructions, and generation parameters.

**File:** `Modelfile`

    # Specify the base model
    FROM qwen3:0.6B
    
    # Set the system prompt (Persona)
    SYSTEM """You are a specialized DevOps assistant. 
    Always provide concise answers and explain technical terms 
    briefly using bullet points."""
    
    # Adjust model parameters
    PARAMETER temperature 0.7

### 3. Build the Custom Model

Since Ollama runs inside a container, the Modelfile must be moved into the container's file system before the build command is executed.

Copy this file into the container

    podman cp Modelfile ollama:/tmp/Modelfile

and create the container `custom-qwen`:

    podman exec -it ollama ollama create custom-qwen -f /tmp/Modelfile

Verify the new model exists:

    podman exec -it ollama ollama list

### 4. Integration with Python

Once the model is created, you can call it via the Ollama API. The system prompt is now "baked into" the model, so your API payload remains clean.

**Example Python Snippet:**

    import requests
    import json
    
    OLLAMA_API_URL = "http://localhost:11434/api/generate"
    
    MODEL_NAME = "custom-qwen"
    payload = {
    "model": MODEL_NAME,
    "prompt": "Explain the advantages of Podman over Docker.",
    "stream": False
    }
    
    response = requests.post(OLLAMA_API_URL, json=payload)
    print(response.json().get("response"))


### 5. Useful Commands
Get Ollama help:

    podman exec -it ollama ollama help

List Ollama models in the container:

    podman exec -it ollama ollama list

Remove Ollama model:

    podman exec -it ollama ollama rm custom-qwen:latest


Written with [StackEdit](https://stackedit.io/).

