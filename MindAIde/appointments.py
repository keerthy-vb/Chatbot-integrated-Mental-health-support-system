from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from bson.objectid import ObjectId

appointments_bp = Blueprint('appointments', __name__)

# 1. Therapist Suggestions for Patients
@appointments_bp.route('/therapist_suggestions')
def therapist_suggestions():
    if 'user_id' not in session:
        flash("Please log in to view therapists.", "danger")
        return redirect(url_for('login'))

    db = current_app.config['DB']

    # ✅ Correct collection: fetch from users collection
    therapists = list(db.users.find({
        "role": {"$regex": "^therapist$", "$options": "i"},
        "verified": True
    }))

    # 🛠 Debug print (optional): Confirm therapists are fetched correctly
    for therapist in therapists:
        print(">>> THERAPIST FROM USERS COLLECTION:", therapist)

    # 🟡 Get user's previous appointment requests
    appointment_requests = list(db.appointments.find({
        "patient_id": ObjectId(session['user_id'])
    }))

    return render_template(
        'therapist_suggestions.html',
        therapists=therapists,
        requests=appointment_requests
    )


# 2. Request an Appointment
@appointments_bp.route('/request_appointment/<therapist_id>', methods=['POST'])
def request_appointment(therapist_id):
    if 'user_id' not in session:
        flash("Please log in to request an appointment.", "danger")
        return redirect(url_for('login'))

    db = current_app.config['DB']
    patient_id = session['user_id']

    # ✅ Check if an appointment already exists
    existing_request = db.appointments.find_one({
        "patient_id": ObjectId(patient_id),
        "therapist_id": ObjectId(therapist_id)
    })

    if existing_request:
        flash("You have already requested an appointment with this therapist.", "warning")
        return redirect(url_for('appointments.therapist_suggestions'))

    # ✅ Insert new appointment request
    db.appointments.insert_one({
        "patient_id": ObjectId(patient_id),
        "therapist_id": ObjectId(therapist_id),
        "status": "Pending"
    })

    flash("Appointment request sent!", "success")
    return redirect(url_for('appointments.therapist_suggestions'))


# 3. Therapist Accept/Reject Appointment
@appointments_bp.route('/update_appointment/<appointment_id>/<action>', methods=['POST'])
def update_appointment(appointment_id, action):
    if 'therapist_id' not in session:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('login'))

    db = current_app.config['DB']
    status = "Accepted" if action == "accept" else "Rejected"

    db.appointments.update_one(
        {"_id": ObjectId(appointment_id)},
        {"$set": {"status": status}}
    )

    flash(f"Appointment {status.lower()}!", "success")
    return redirect(url_for('appointments.therapist_dashboard'))


# 4. Therapist Dashboard (View Appointment Requests)
@appointments_bp.route('/therapist_dashboard')
def therapist_dashboard():
    if 'therapist_id' not in session:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('login'))

    db = current_app.config['DB']
    therapist_id = session['therapist_id']

    requests = list(db.appointments.find({
        "therapist_id": ObjectId(therapist_id)
    }))

    return render_template('therapist_dashboard.html', requests=requests)
