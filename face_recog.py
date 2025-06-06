# face_recog.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from db import find_all_users

def recognize_face(face_embedding, threshold=0.6):
    users = find_all_users()
    best_match = None
    highest_sim = 0

    for user in users:
        stored_emb = np.array(user["embedding"]).reshape(1, -1)
        sim = cosine_similarity(stored_emb, face_embedding.reshape(1, -1))[0][0]
        if sim > threshold and sim > highest_sim:
            best_match = user
            highest_sim = sim

    return best_match
