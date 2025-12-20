import cv2
from ultralytics import YOLO
import numpy as np
import os
import time

# --- Konfiguration ---
PIPE_PATH = '/tmp/vlc_pipe'
CAM_INDEX = 0  # /dev/video2
WIDTH = 320
HEIGHT = 256
FPS = 10 # Entspricht der Einstellung im VLC-Befehl

# --- Initialisierung ---
try:
	# 1. YOLOv8 Pose Modell laden (z.B. nano-Version für Geschwindigkeit)
	# Pose-Modelle erkennen Keypoints (Körper, aber funktioniert oft gut genug für Haupt-Gesichtspunkte)
	model = YOLO('yolov8n-pose.pt') 

	# 2. Kamera öffnen
	cap = cv2.VideoCapture(CAM_INDEX)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
	cap.set(cv2.CAP_PROP_FPS, FPS)

	if not cap.isOpened():
		print(f"FEHLER: Kamera {CAM_INDEX} konnte nicht geöffnet werden.")
		exit()

	# 3. Named Pipe zum Schreiben öffnen
	# 'wb' = write binary
	pipe = os.open(PIPE_PATH, os.O_WRONLY)

except Exception as e:
	print(f"Initialisierungsfehler: {e}")
	exit()

print(f"YOLO-Verarbeitung und Streaming über Pipe {PIPE_PATH} gestartet...")

# --- Hauptschleife ---
while True:
	ret, frame = cap.read()
	if not ret:
		print("Kamerafehler: Frame konnte nicht gelesen werden.")
		break

	# 4. YOLOv8-Erkennung (nur Keypoints)
	# Konfidenz auf 0.5 setzen, und nur Keypoints anzeigen
	results = model(frame, conf=0.5, show_labels=False, show_conf=False, stream=True)

	# 5. Verarbeitung der Ergebnisse
	annotated_frame = frame.copy()

	# Keypoint-Indices für wichtige Gesichtspunkte im YOLO-Pose-Modell:
	# 1: Nase (oft erkannt)
	# 2-5: Augen/Ohren (können in dieser Reihenfolge liegen, erfordert Feintuning)
	# 6: Linkes Handgelenk, etc. (Wir müssen uns auf die Kopf-Punkte konzentrieren)

	relevant_points = []

	for r in results:
    
		# ALT: if r.keypoints and r.keypoints.x.numel() > 0:
		if r.keypoints and r.keypoints.xy.numel() > 0:
			# Keypoints sind jetzt im Format [N Detections, M Keypoints, 2 (x,y)]
			keypoints = r.keypoints.xy[0].cpu().numpy() # Keypoints des ersten gefundenen Objekts

			# Die Struktur von keypoints ist nun: [[x1, y1], [x2, y2], ..., [xm, ym]]

			# Datenextraktion (Beispiel: Nase und Augen)
			# YOLO Pose liefert 17 Punkte, wir greifen auf die ersten zu:
			if len(keypoints) >= 5:

				# 1. Nase (Index 0)
				nase = keypoints[0] # [x, y]

				#  2. Linkes Auge (Index 1) und Rechtes Auge (Index 2)
				linkes_auge = keypoints[1]
				rechtes_auge = keypoints[2]

				# --- B) Keypoints auf das Bild zeichnen (Overlay) ---
				# Zeichnen der Nase:
				cv2.circle(annotated_frame, (int(nase[0]), int(nase[1])), 5, (0, 0, 255), -1) 

				# Zeichnen der Augen:
				cv2.circle(annotated_frame, (int(linkes_auge[0]), int(linkes_auge[1])), 3, (0, 255, 0), -1) 
				cv2.circle(annotated_frame, (int(rechtes_auge[0]), int(rechtes_auge[1])), 3, (0, 255, 0), -1) 

				# ... Hier müsste die Logik zur seriellen Übertragung an den Arduino/LLM folgen ...

		# Wir verlassen die Schleife nach dem ersten gefundenen Gesicht
		break


	# 6. Bild in die Pipe schreiben
	try:
		# Die Daten müssen als unkomprimierte BGR3-Bytes in die Pipe geschrieben werden
		os.write(pipe, annotated_frame.tobytes())
	except BrokenPipeError:
		# Tritt auf, wenn VLC beendet wird.
		print("FEHLER: Broken Pipe. VLC wurde beendet oder hängt.")
		break
	except Exception as e:
		# Andere Schreibfehler
		print(f"Schreibfehler in Pipe: {e}")
		break

	# Begrenzung der Framerate (optional, wenn YOLO zu schnell ist)
	time.sleep(1/FPS)

# --- Aufräumarbeiten ---
os.close(pipe)
cap.release()
print("Pipeline beendet.")

