# main_recog.py
import cv2
from insightface.app import FaceAnalysis
from db import mark_attendance
from face_recog import recognize_face

# Initialize face recognition model
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0)

# Track users already marked today
marked_today = set()

def start_recognition():
    cap = cv2.VideoCapture(0)
    print("🎥 Starting face recognition... Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect faces in frame
        faces = app.get(frame)
        for face in faces:
            bbox = face.bbox.astype(int)
            cv2.rectangle(frame, tuple(bbox[:2]), tuple(bbox[2:]), (0, 255, 0), 2)

            # Recognize face
            match = recognize_face(face.embedding)
            if match:
                user_id = match["user_id"]
                name = match["name"]
                role = match["role"]

                # Mark attendance only once per user per day
                if user_id not in marked_today:
                    mark_attendance(user_id)
                    marked_today.add(user_id)
                    print(f"✅ Attendance marked for {name} ({role})")

                # Show label on screen
                label = f"{name} ({role})"
                cv2.putText(frame, label, (bbox[0], bbox[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Show video feed
        cv2.imshow("Face Recognition", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_recognition()
