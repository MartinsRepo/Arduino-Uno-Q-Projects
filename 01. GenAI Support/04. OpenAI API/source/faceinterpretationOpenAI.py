import cv2
import mediapipe as mp
import subprocess
import json
import threading
import os
import base64
import textwrap
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# --- LOAD ENVIRONMENT VARIABLES ---
load_dotenv()
open_api_key = os.getenv('OPENAI_API_KEY')

# --- CONFIGURATION ---
WIDTH, HEIGHT = 320, 240
FPS = 20
DESTINATION = "udp://192.168.0.228:8080"
VIDEO = 0

vision_llm = ChatOpenAI(model="gpt-4o", api_key=open_api_key, temperature=0.5)

# Global variables
is_processing = False
last_prediction = "Waiting for AI..." # Stores the text to display on screen

# FFmpeg Setup
ffmpeg_cmd = [
    'ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo',
    '-pix_fmt', 'bgr24', '-s', f"{WIDTH}x{HEIGHT}", '-r', str(FPS),
    '-i', '-',
    '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency',
    '-profile:v', 'baseline', '-g', '10', '-b:v', '1M',
    '-pix_fmt', 'yuv420p', '-f', 'mpegts', DESTINATION
]

pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
cap = cv2.VideoCapture(VIDEO)

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=0, color=(0, 255, 0))

def ask_openai_worker(landmark_json, base64_image):
    global is_processing, last_prediction
    
    # We explicitly tell the AI we don't want identification to avoid safety triggers
    system_prompt = (
        "You are an expert in facial expression analysis. "
        "Your task is to describe facial movements and emotions ONLY. "
        "DO NOT attempt to identify the person. If you see a face, focus on the "
        "muscle movements, eyes, mouth, and head pose. Be very concise (1 short sentence)."
    )
    
    message = HumanMessage(content=[
        {
            "type": "text", 
            "text": f"Analyze the expression based on these landmarks {landmark_json} and the image. What is the current emotion or pose?"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
                "detail": "low"  # 'low' detail often bypasses strict facial recognition triggers
            }
        }
    ])
    
    try:
        response = vision_llm.invoke([SystemMessage(content=system_prompt), message])
        last_prediction = response.content.strip()
    except Exception as e:
        last_prediction = "AI Analysis paused..."
    finally:
        is_processing = False

with mp_face_mesh.FaceMesh(refine_landmarks=True) as face_mesh:
    while cap.isOpened():
        success, frame = cap.read()
        if not success: break
        
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        ai_frame = frame.copy()
        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # 1. Start AI Thread
                if not is_processing:
                    is_processing = True
                    _, buffer = cv2.imencode('.jpg', ai_frame)
                    base64_img = base64.b64encode(buffer).decode('utf-8')
                    thread = threading.Thread(target=ask_openai_worker, args=("{}", base64_img))
                    thread.daemon = True
                    thread.start()

                # 2. Draw Mesh
                mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS, None, drawing_spec)

        # --- TEXT OVERLAY LOGIC ---
        # Wrap text to fit the small 320x240 screen
        wrapped_text = textwrap.wrap(last_prediction, width=40) 
        
        for i, line in enumerate(wrapped_text):
            # Move the starting Y-position based on the number of lines
            # Using a smaller fontScale (0.35) and thinner lines (1)
            y_coord = (HEIGHT - 50) + (i * 12) 
            
            # Subtitle-style: Black outline/shadow for readability
            cv2.putText(frame, line, (11, y_coord + 1), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 0), 2, cv2.LINE_AA)
            
            # Main white text
            cv2.putText(frame, line, (10, y_coord), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1, cv2.LINE_AA)

        try:
            pipe.stdin.write(frame.tobytes())
        except:
            break

cap.release()
pipe.stdin.close()

