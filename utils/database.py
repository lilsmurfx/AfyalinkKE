from supabase_config import supabase
from datetime import datetime
import uuid

# -----------------------
# Users / Admin functions
# -----------------------
def get_all_users():
    """Return all users"""
    res = supabase.table("users").select("*").execute()
    return res.data if res.data else []

def get_all_patients():
    """Return all patients"""
    res = supabase.table("patients").select("*").execute()
    return res.data if res.data else []

def add_patient(name: str, age: int, doctor_id: str, create_user: bool = True):
    """
    Add a new patient and optionally create a user account for them.
    - create_user=True: also adds patient to 'users' table for login.
    """
    # Insert into patients table
    supabase.table("patients").insert({
        "name": name,
        "age": age,
        "doctor_id": doctor_id,
        "created_at": datetime.utcnow()
    }).execute()

    # Optional: create a login user for the patient
    if create_user:
        # Check if user already exists
        existing = supabase.table("users").select("*").eq("full_name", name).execute()
        if not existing.data:
            supabase.table("users").insert({
                "full_name": name,
                "role": "patient",
                "email": "",  # Optionally add email
                "password": ""  # Add default or random password handling
            }).execute()

def get_user_name(user_id: str):
    """Return the full name of a user given their user_id"""
    res = supabase.table("users").select("full_name").eq("id", user_id).single().execute()
    return res.data["full_name"] if res.data else "User"

# -----------------------
# Doctor functions
# -----------------------
def get_doctor_patients(doctor_id: str):
    """Get all patients assigned to a doctor"""
    res = supabase.table("patients").select("*").eq("doctor_id", doctor_id).execute()
    return res.data if res.data else []

def add_record(patient_id: str, title: str, description: str):
    """Add a medical record for a patient"""
    supabase.table("medical_records").insert({
        "patient_id": patient_id,
        "record_title": title,
        "description": description,
        "created_at": datetime.utcnow()
    }).execute()

def add_appointment(doctor_id: str, patient_id: str, appointment_time: datetime):
    """Add a new appointment"""
    supabase.table("appointments").insert({
        "doctor_id": doctor_id,
        "patient_id": patient_id,
        "appointment_time": appointment_time.isoformat(),
        "status": "scheduled",
        "created_at": datetime.utcnow()
    }).execute()

# -----------------------
# Appointments / Patients
# -----------------------
def get_user_appointments(user_id: str, role: str):
    """Get appointments for a doctor or patient"""
    if role == "doctor":
        res = supabase.table("appointments").select("*").eq("doctor_id", user_id).execute()
    else:
        res = supabase.table("appointments").select("*").eq("patient_id", user_id).execute()
    return res.data if res.data else []

# -----------------------
# Patient records
# -----------------------
def get_patient_records(patient_id: str):
    """Get medical records for a patient"""
    res = supabase.table("medical_records").select("*").eq("patient_id", patient_id).execute()
    return res.data if res.data else []

# -----------------------
# Admin / Unassign
# -----------------------
def unassign_patient(patient_id: str):
    """Remove doctor assignment from patient"""
    supabase.table("patients").update({"doctor_id": None}).eq("id", patient_id).execute()

# -----------------------
# Patient File Uploads
# -----------------------
def upload_patient_file(patient_id: str, file):
    """Upload a patient's file to Supabase Storage and save record in DB"""
    if not file:
        return None

    # Generate a unique filename
    file_ext = file.name.split('.')[-1]
    file_name = f"{patient_id}/{uuid.uuid4()}.{file_ext}"

    # Upload to storage bucket "patient-files"
    res = supabase.storage.from_('patient-files').upload(file_name, file)

    if res.status_code in [200, 201]:
        # Save file metadata in DB
        supabase.table('patient_files').insert({
            "patient_id": patient_id,
            "file_name": file_name,
            "original_name": file.name,
            "uploaded_at": datetime.utcnow().isoformat()
        }).execute()
        return file_name
    else:
        raise Exception("Upload failed")

def get_patient_files(patient_id: str):
    """Return all files uploaded by a patient"""
    res = supabase.table('patient_files').select("*").eq("patient_id", patient_id).execute()
    return res.data if res.data else []
