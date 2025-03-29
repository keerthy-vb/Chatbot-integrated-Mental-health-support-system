from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from bson.objectid import ObjectId
 # Import database connection

appointments_bp = Blueprint('appointments', __name__)

# 2.1 Route: View therapist suggestions
@appointments_bp.route('/therapist_suggestions')
def therapist_suggestions():
    if 'user_id' not in session:
        flash("Please log in to view therapists.", "danger")
        return redirect(url_for('login'))

    therapists = list(db.therapists.find({"verified": True}))
    user_id = session['user_id']
    appointment_requests = list(db.appointments.find({"patient_id": ObjectId(user_id)}))

    return render_template('therapist_suggestions.html', therapists=therapists, requests=appointment_requests)


# 2.2 Route: Request an appointment
@appointments_bp.route('/request_appointment/<therapist_id>', methods=['POST'])
def request_appointment(therapist_id):
    if 'user_id' not in session:
        flash("Please log in to request an appointment.", "danger")
        return redirect(url_for('login'))

    patient_id = session['user_id']

    existing_request = db.appointments.find_one({"patient_id": ObjectId(patient_id), "therapist_id": ObjectId(therapist_id)})
    if existing_request:
        flash("You have already requested an appointment with this therapist.", "warning")
        return redirect(url_for('appointments.therapist_suggestions'))

    db.appointments.insert_one({
        "patient_id": ObjectId(patient_id),
        "therapist_id": ObjectId(therapist_id),
        "status": "Pending"
    })

    flash("Appointment request sent!", "success")
    return redirect(url_for('appointments.therapist_suggestions'))


# 2.3 Route: Therapist Accept/Reject appointment
@appointments_bp.route('/update_appointment/<appointment_id>/<action>', methods=['POST'])
def update_appointment(appointment_id, action):
    if 'therapist_id' not in session:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('login'))

    status = "Accepted" if action == "accept" else "Rejected"

    db.appointments.update_one({"_id": ObjectId(appointment_id)}, {"$set": {"status": status}})

    flash(f"Appointment {status.lower()}!", "success")
    return redirect(url_for('appointments.therapist_dashboard'))


# 2.4 Route: Therapist Dashboard (To View Requests)
@appointments_bp.route('/therapist_dashboard')
def therapist_dashboard():
    if 'therapist_id' not in session:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('login'))

    therapist_id = session['therapist_id']
    requests = list(db.appointments.find({"therapist_id": ObjectId(therapist_id)}))

    return render_template('therapist_dashboard.html', requests=requests)
