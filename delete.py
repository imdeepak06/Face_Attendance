from db import users_col

def delete_user():
    user_id = input("Enter the ID of the user to delete: ")
    user = users_col.find_one({"user_id": user_id})
    
    if user:
        print(f"Found user: {user['name']} ({user['role']})")
        confirm = input("Are you sure you want to delete this user? (y/n): ").lower()
        if confirm == 'y':
            users_col.delete_one({"user_id": user_id})
            print("User deleted.")
        else:
            print("Operation cancelled.")
    else:
        print("User not found.")

if __name__ == "__main__":
    delete_user()