# db.py
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["face_attendance"]
users_col = db["users"]
attendance_col = db["attendance"]

def save_user(name, user_id, role, embedding):
    users_col.insert_one({
        "name": name,
        "user_id": user_id,
        "role": role.lower(),
        "embedding": embedding.tolist()
    })

def find_all_users():
    return list(users_col.find())

def mark_attendance(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    already_marked = attendance_col.find_one({
        "user_id": user_id,
        "date": today
    })
    if not already_marked:
        attendance_col.insert_one({
            "user_id": user_id,
            "date": today,
            "time": datetime.now().strftime("%H:%M:%S"),
            "status": "Present"
        })

def get_today_attendance():
    today = datetime.now().strftime("%Y-%m-%d")
    return list(attendance_col.find({"date": today}))

def get_user_by_id(user_id):
    return users_col.find_one({"user_id": user_id})

def get_all_users():
    return list(users_col.find({}, {"_id": 0, "name": 1, "user_id": 1, "role": 1}))

