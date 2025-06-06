# register_face.py
import cv2
import numpy as np
from insightface.app import FaceAnalysis
from db import save_user

# Use buffalo_l model (fast and reliable)
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0)

def register():
    name = input("Enter name: ")
    user_id = input("Enter ID: ")
    role = input("Enter role (student/staff): ").lower()

    cap = cv2.VideoCapture(0)
    print("\nAdjust your face. Press 'S' to capture (do 3–5 times from different angles, open mouth, etc). Press 'Q' when done.\n")

    embeddings = []
    captured = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = app.get(frame)
        for face in faces:
            bbox = face.bbox.astype(int)
            cv2.rectangle(frame, tuple(bbox[:2]), tuple(bbox[2:]), (0, 255, 0), 2)
            cv2.putText(frame, "Press 'S' to capture", (bbox[0], bbox[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Register Face", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s') and faces:
            embeddings.append(faces[0].embedding)
            captured += 1
            print(f"[{captured}] Face embedding captured.")
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if embeddings:
        avg_embedding = np.mean(embeddings, axis=0)
        save_user(name, user_id, role, avg_embedding)
        print(f"✅ {captured} captures done. User '{name}' registered successfully.")
    else:
        print("❌ No face embeddings captured. Try again.")

if __name__ == "__main__":
    register()
