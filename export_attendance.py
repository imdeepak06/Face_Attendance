# export_attendance.py
import os
import csv
from datetime import datetime
from db import get_today_attendance, get_all_users

def format_time_ist(time_str):
    try:
        time_obj = datetime.strptime(time_str, "%H:%M:%S")
        return time_obj.strftime("%I:%M %p")  # 12-hour format with AM/PM
    except:
        return "-"  # If time is "-", return as-is

def export_attendance():
    today = datetime.now().strftime("%Y-%m-%d")
    student_path = os.path.join("student_attendance", f"{today}.csv")
    staff_path = os.path.join("staff_attendance", f"{today}.csv")

    os.makedirs("student_attendance", exist_ok=True)
    os.makedirs("staff_attendance", exist_ok=True)

    students = []
    staff = []

    # Get all users and today's attendance
    all_users = get_all_users()
    attendance_records = get_today_attendance()
    present_dict = {record["user_id"]: record["time"] for record in attendance_records}

    for user in all_users:
        raw_time = present_dict.get(user["user_id"], "-")
        time_in = format_time_ist(raw_time)
        status = "Present" if user["user_id"] in present_dict else "Absent"
        row = [user["name"], user["user_id"], time_in, status]

        if user["role"] == "student":
            students.append(row)
        else:
            staff.append(row)

    # Write student CSV
    with open(student_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "ID", "Time-In", "Status"])
        writer.writerows(students)

    # Write staff CSV
    with open(staff_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "ID", "Time-In", "Status"])
        writer.writerows(staff)

    print("✅ Attendance exported successfully.")

if __name__ == "__main__":
    export_attendance()
