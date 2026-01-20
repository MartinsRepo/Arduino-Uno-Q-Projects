import cv2
import mediapipe as mp
import subprocess

# --- KONFIGURATION ---
WIDTH, HEIGHT = 320, 240
FPS = 20
DESTINATION = "udp://192.168.0.228:8080"

# FFmpeg Setup (Robust für Netzwerk-Streaming)
#ffmpeg_cmd = [
#    'ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo',
#    '-pix_fmt', 'bgr24', '-s', f"{WIDTH}x{HEIGHT}", '-r', str(FPS),
#    '-i', '-',
#    '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency',
#    '-profile:v', 'baseline', '-g', '10', '-b:v', '1M',
#    '-pix_fmt', 'yuv420p', '-f', 'mpegts', DESTINATION
#]

ffmpeg_cmd = [
    'ffmpeg', '-y', 
    '-f', 'rawvideo', '-vcodec', 'rawvideo',
    '-pix_fmt', 'bgr24', '-s', f"{WIDTH}x{HEIGHT}", '-r', str(FPS),
    '-i', '-',
    # Neuer Teil: Zeitstempel glätten und Video kodieren
    '-vf', 'setpts=N/FRAME_RATE/TB', 
    '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency',
    '-profile:v', 'baseline', '-g', '10', '-b:v', '1M',
    # Erzwinge konstante Framerate im Output
    '-r', str(FPS), 
    '-pix_fmt', 'yuv420p', '-f', 'mpegts', 
    DESTINATION
]

pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
cap = cv2.VideoCapture(2)

# MediaPipe Setup
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
# Wir definieren einen feinen Zeichenstil
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=0, color=(0, 255, 0))

with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True, # Aktiviert detaillierte Augen/Lippen-Punkte
    min_detection_confidence=0.5) as face_mesh:

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break
        
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                
                # 1. Gesichtsoval zeichnen
                mp_drawing.draw_landmarks(
                    image=frame, landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_FACE_OVAL,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=drawing_spec)

                # 2. Augen (Links & Rechts) und Brauen
                for connection_set in [mp_face_mesh.FACEMESH_LEFT_EYE, 
                                       mp_face_mesh.FACEMESH_RIGHT_EYE,
                                       mp_face_mesh.FACEMESH_LEFT_EYEBROW,
                                       mp_face_mesh.FACEMESH_RIGHT_EYEBROW]:
                    mp_drawing.draw_landmarks(
                        image=frame, landmark_list=face_landmarks,
                        connections=connection_set,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=drawing_spec)

                # 3. Lippen / Mund
                mp_drawing.draw_landmarks(
                    image=frame, landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_LIPS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=drawing_spec)

                # Nasenrücken und Nasenflügel (manuelle Indizes für eine klare Linie)
                nose_indices = [
                        (168, 6), (6, 197), (197, 195), (195, 5), # Nasenrücken vertikal
                        (102, 64), (64, 98), (98, 97),             # Nasenflügel links
                        (331, 294), (294, 327), (327, 326)         # Nasenflügel rechts
                ]

                for start_idx, end_idx in nose_indices:
                        start_point = face_landmarks.landmark[start_idx]
                        end_point = face_landmarks.landmark[end_idx]

                # Umrechnung der normierten Koordinaten in Pixel
                pt1 = (int(start_point.x * WIDTH), int(start_point.y * HEIGHT))
                pt2 = (int(end_point.x * WIDTH), int(end_point.y * HEIGHT))

                cv2.line(frame, pt1, pt2, (0, 255, 0), 1)

                # 4. Nase (optional, Landmarks manuell verbinden oder Kontur nutzen)
                # Da FACEMESH_NOSE nicht in allen Versionen als fertiges Set existiert,
                # nutzen wir FACEMESH_CONTOURS gefiltert oder belassen es bei den Augen/Mund.

        try:
            pipe.stdin.write(frame.tobytes())
        except:
            break

cap.release()
pipe.stdin.close()

