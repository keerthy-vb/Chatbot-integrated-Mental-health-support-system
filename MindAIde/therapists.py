from flask import Blueprint, render_template, request, redirect, url_for, flash
from pymongo import MongoClient

therapists_bp = Blueprint('therapists', __name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mental_health_db"]
therapists_collection = db["therapists"]
appointments_collection = db["appointments"]

@therapists_bp.route('/therapists')
def view_therapists():
    therapists = therapists_collection.find()  # Fetch all therapists
    return render_template('therapist_suggestions.html', therapists=therapists)

@therapists_bp.route('/request_appointment', methods=['POST'])
def request_appointment():
    patient_name = request.form.get("patient_name")
    therapist_id = request.form.get("therapist_id")

    appointment_data = {
        "patient_name": patient_name,
        "therapist_id": therapist_id,
        "status": "Pending"
    }
    
    appointments_collection.insert_one(appointment_data)
    flash("Appointment request sent successfully!", "success")
    return redirect(url_for('therapists.view_therapists'))
