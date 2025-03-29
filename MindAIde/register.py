from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import re

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_db"]
users = db["users"]

# Password validation pattern
PASSWORD_PATTERN = re.compile(r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data["name"]
    role = data["role"]
    email = data["email"]
    password = data["password"]

    # Check if email is already registered
    if users.find_one({"email": email}):
        return jsonify({"success": False, "message": "⚠️ Email already registered!"})

    # Validate password strength
    if not PASSWORD_PATTERN.match(password):
        return jsonify({"success": False, "message": "⚠️ Password does not meet security requirements!"})

    # Hash password before saving
    hashed_password = generate_password_hash(password)

    user_data = {
        "name": name,
        "role": role,
        "email": email,
        "password": hashed_password
    }

    # Caretaker validation: Check if patient email exists
    if role == "caretaker":
        patient_email = data.get("patient_email")
        if not users.find_one({"email": patient_email, "role": "patient"}):
            return jsonify({"success": False, "message": "⚠️ No patient found with this email!"})
        user_data["patient_email"] = patient_email

    users.insert_one(user_data)
    return jsonify({"success": True, "message": "✅ Account created successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
