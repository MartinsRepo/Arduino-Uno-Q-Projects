import requests
import time
from arduino.app_utils import *

# Probieren Sie die Host-IP oder das Gateway 172.17.0.1
DOCKER_URL = "http://172.17.0.1:5000/data" 

def loop():
    try:
        # Erhöhen Sie den Timeout auf 5 Sekunden! 
        # OpenAI und MediaPipe brauchen Zeit.
        response = requests.get(DOCKER_URL, timeout=5.0) 
        
        if response.status_code == 200:
            ai_text = response.text
            print(f"Empfangen: {ai_text}") # Debugging im App Lab Log
            Bridge.call("display_print", ai_text)
        else:
            Bridge.call("display_print", "Server Error")
            
    except requests.exceptions.Timeout:
        # Falls der AI-Worker noch rechnet, einfach kurz warten
        Bridge.call("display_print", "AI is busy...")
    except Exception as e:
        Bridge.call("display_print", "Link Lost")
        time.sleep(2)
    
    time.sleep(1.0) # Etwas mehr Pause zwischen den Abfragen

App.run(user_loop=loop)