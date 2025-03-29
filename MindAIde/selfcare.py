from flask import Blueprint, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime, timedelta
import threading
import time

# Initialize Flask Blueprint
selfcare_bp = Blueprint("selfcare", __name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_db"]
suggestions_collection = db["selfcare_suggestions"]
reminders_collection = db["reminders"]

@selfcare_bp.route("/", methods=["GET"])
def selfcare_home():
    return render_template("selfcare.html")


# Fetch self-care suggestions based on category
@selfcare_bp.route("/get_suggestions", methods=["GET"])
def get_suggestions():
    category = request.args.get("category")
    if not category:
        return jsonify({"error": "Category is required"}), 400

    suggestions = list(suggestions_collection.find({"category": category}, {"_id": 0}))
    return jsonify(suggestions)

# Save selected activity with a reminder
@selfcare_bp.route("/save_activity", methods=["POST"])
def save_activity():
    data = request.json
    user_id = data.get("user_id")  # Assume user ID is passed
    title = data.get("title")
    reminder_time = data.get("reminder_time")  # Format: "YYYY-MM-DD HH:MM"

    if not user_id or not title or not reminder_time:
        return jsonify({"error": "Missing required fields"}), 400

    reminder = {
        "user_id": user_id,
        "title": title,
        "reminder_time": datetime.strptime(reminder_time, "%Y-%m-%d %H:%M"),
        "status": "pending"
    }
    reminders_collection.insert_one(reminder)
    return jsonify({"message": "Activity saved with reminder!"}), 201

# Mark activity as Done or Missed
@selfcare_bp.route("/update_activity_status", methods=["POST"])
def update_activity_status():
    data = request.json
    user_id = data.get("user_id")
    title = data.get("title")
    status = data.get("status")  # "Done" or "Missed"

    if not user_id or not title or status not in ["Done", "Missed"]:
        return jsonify({"error": "Invalid input"}), 400

    reminders_collection.update_one(
        {"user_id": user_id, "title": title},
        {"$set": {"status": status}}
    )
    return jsonify({"message": "Activity status updated successfully!"}), 200

# Function to send notifications
def send_reminders():
    while True:
        current_time = datetime.now()
        pending_reminders = reminders_collection.find({"status": "pending"})

        for reminder in pending_reminders:
            reminder_time = reminder["reminder_time"]
            if current_time >= reminder_time:
                print(f"🔔 Reminder for {reminder['user_id']}: {reminder['title']} is due!")
                reminders_collection.update_one(
                    {"_id": reminder["_id"]},
                    {"$set": {"status": "notified"}}
                )
        
        time.sleep(60)  # Check every minute

# Run reminder checking in the background
reminder_thread = threading.Thread(target=send_reminders, daemon=True)
reminder_thread.start()
