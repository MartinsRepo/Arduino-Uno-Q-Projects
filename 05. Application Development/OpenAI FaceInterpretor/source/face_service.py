import cv2
import mediapipe as mp
import threading
import base64
import os
import json
from flask import Flask, Response
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from datetime import datetime
from threading import Lock

load_dotenv()

app = Flask(__name__)

class FaceEngine:
    def __init__(self):
        self.processing_lock = Lock()
        self.last_prediction = "Waiting for face..."
        self.current_frame = None  # Speicher für den MJPEG Stream
        
        # Kamera-Setup für Video2 (Microsoft LifeCam)
        self.cap = cv2.VideoCapture("/dev/video2", cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        )

        self.model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.5,
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def _ai_worker(self, landmark_json, img_b64):
        system_prompt = (
            "Describe visible facial muscle movements and geometry only. "
            "Do NOT infer emotion, intent, or identity. "
            "Max 6 words."
        )

        try:
            message = HumanMessage(
                content=[
                    {"type": "text", "text": f"Landmarks: {landmark_json}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            )

            response = self.model.invoke([
                SystemMessage(content=system_prompt),
                message
            ])

            ai_text = str(response.content).strip()
            now = datetime.now().strftime("%H:%M:%S")
            self.last_prediction = f"[{now}] {ai_text}"

        except Exception as e:
            self.last_prediction = f"AI ERROR: {str(e)[:20]}"
        finally:
            if self.processing_lock.locked():
                self.processing_lock.release()

    def process(self):
        if not self.cap.isOpened():
            return self.last_prediction

        success, frame = self.cap.read()
        if not success:
            return self.last_prediction

        # Frame für den MJPEG Stream bereitstellen (mit Overlay)
        display_frame = frame.copy()
        cv2.putText(display_frame, self.last_prediction, (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # In JPEG kodieren für den Browser-Stream
        ret, jpeg = cv2.imencode('.jpg', display_frame)
        if ret:
            self.current_frame = jpeg.tobytes()

        # AI Logik
        if not self.processing_lock.acquire(blocking=False):
            return self.last_prediction 

        results = self.face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        landmarks = [
            {"x": round(l.x, 3), "y": round(l.y, 3), "z": round(l.z, 3)}
            for l in results.multi_face_landmarks[0].landmark
        ] if results.multi_face_landmarks else None

        if landmarks:
            _, buffer = cv2.imencode(".jpg", cv2.resize(frame, (320, 240)))
            img_b64 = base64.b64encode(buffer).decode("utf-8")

            threading.Thread(
                target=self._ai_worker,
                args=(json.dumps(landmarks[::10]), img_b64),
                daemon=True
            ).start()
        else:
            self.processing_lock.release()

        return self.last_prediction

engine = FaceEngine()

def gen_frames():
    """Generator für den MJPEG Stream."""
    while True:
        engine.process() # Kamera triggern
        if engine.current_frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + engine.current_frame + b'\r\n')

@app.route("/video_feed")
def video_feed():
    """Video Streaming Route."""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/data")
def get_data():
    """Endpoint für die Arduino-Textdaten."""
    return engine.last_prediction

if __name__ == "__main__":
    if not engine.cap.isOpened():
        print("CRITICAL: Camera not found.")
    # Threaded=True ist wichtig, damit Flask Stream und Daten gleichzeitig bedienen kann
    app.run(host="0.0.0.0", port=5000, threaded=True)