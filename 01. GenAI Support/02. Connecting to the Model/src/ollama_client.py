import requests
import json

# --- Configuration ---
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:0.6B"  # use this model
PROMPT_TEXT = "Explain in short terms, what the usecase of podman is and the advantages compared with Docker."

def generate_response(prompt: str, model: str):
    """
    Publishes a prompt at the  Ollama APIand returns the answer.
    """
    
    # 1. Datastructure for the API in JSON format
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False  # Wait for the complete answert
    }

    print(f"Publishing query to '{model}'...")
    
    try:
        # 2. HTTP POST call to the port of the Podman container
        response = requests.post(
            OLLAMA_API_URL, 
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"}
        )
        
        # 3. Check of the HTTP status
        if response.status_code == 200:
            data = response.json()
            
            # 4. Extrahieren der Antwort aus der JSON-Struktur
            generated_text = data.get("response", "No answer found.")
            
            return generated_text
        else:
            return (f"API error. Statuscode: {response.status_code}\n"
                    f"Resonse text: {response.text}")

    except requests.exceptions.ConnectionError:
        return (f"Connection error: Ensure, that the Ollama container is running "
                f"and der port 11434 is mapped to localhost (Podman: 'run -p 11434:11434').")
    except Exception as e:
        return f"Unknown error!: {e}"

# --- Hauptausführung ---
if __name__ == "__main__":
    result = generate_response(PROMPT_TEXT, MODEL_NAME)
    
    print("-" * 50)
    print(f"🧠 Modell: {MODEL_NAME}")
    print(f"💬 Prompt: {PROMPT_TEXT}")
    print("-" * 50)
    print("✅ GENERIERTE ANTWORT:")
    print(result)
    print("-" * 50)

