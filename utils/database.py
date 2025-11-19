# utils/database.py

from supabase_config import supabase
from datetime import datetime
import uuid
from typing import Optional, List


# ============================================================
# USER HELPERS
# ============================================================

def get_user_by_email(email: str) -> Optional[dict]:
    """
    MORE FORGIVING lookup:
    - strips whitespace
    - lowercase email matching
    - works even if DB contains uppercase or hidden spaces
    """

    clean_email = email.strip().lower()

    # Try exact match first
    res = supabase.table("users") \
        .select("*") \
        .eq("email", clean_email) \
        .single() \
        .execute()

    if res.data:
        return res.data

    # Try case-insensitive fallback
    res_fallback = supabase.table("users") \
        .select("*") \
        .execute()

    users = res_fallback.data or []

    for u in users:
        if u.get("email", "").strip().lower() == clean_email:
            return u

    return None


def get_user_name(user_id: str) -> str:
    """Return the user's full name or fallback."""
    try:
        res = supabase.table("users").select("full_name").eq("id", user_id).single().execute()
        if res and res.data:
            return res.data.get("full_name", "User")
    except:
        pass
    return "User"


def get_all_patients():
    res = supabase.table("users").select("*").eq("role", "patient").execute()
    return res.data or []


def get_all_users():
    res = supabase.table("users").select("*").execute()
    return res.data or []


# ============================================================
# DOCTOR & PATIENT FUNCTIONS
# ============================================================

def get_doctor_patients(doctor_id: str) -> List[dict]:
    if not doctor_id:
        return []
    res = supabase.table("patients").select("*").eq("doctor_id", doctor_id).execute()
    return res.data or []


def add_record(patient_id: str, title: str, description: str):
    supabase.table("medical_records").insert({
        "patient_id": patient_id,
        "record_title": title,
        "description": description,
        "created_at": datetime.utcnow().isoformat()
    }).execute()


# ============================================================
# MEDICAL RECORDS
# ============================================================

def get_patient_records(patient_id: str):
    res = supabase.table("medical_records").select("*").eq("patient_id", patient_id).execute()
    records = res.data or []

    for r in records:
        try:
            if isinstance(r.get("created_at"), str):
                r["created_at"] = datetime.fromisoformat(r["created_at"])
        except:
            pass

    return records


# ============================================================
# APPOINTMENTS
# ============================================================

def add_appointment(doctor_id: str, patient_id: str, appointment_time):
    appointment_iso = (
        appointment_time.isoformat()
        if hasattr(appointment_time, "isoformat")
        else str(appointment_time)
    )

    supabase.table("appointments").insert({
        "doctor_id": doctor_id,
        "patient_id": patient_id,
        "appointment_time": appointment_iso,
        "status": "scheduled",
        "created_at": datetime.utcnow().isoformat()
    }).execute()


def get_user_appointments(user_id: str, role: str):
    field = "doctor_id" if role == "doctor" else "patient_id"
    res = supabase.table("appointments").select("*").eq(field, user_id).execute()

    appts = res.data or []

    for a in appts:
        for f in ["appointment_time", "created_at"]:
            try:
                if isinstance(a.get(f), str):
                    a[f] = datetime.fromisoformat(a[f])
            except:
                pass

    return appts


# ============================================================
# ADMIN / UNASSIGN PATIENTS
# ============================================================

def unassign_patient(patient_id: str):
    supabase.table("patients").update({"doctor_id": None}).eq("id", patient_id).execute()


# ============================================================
# FILE UPLOADS
# ============================================================

def upload_patient_file(patient_id: str, file, user_token=None):
    if not file:
        return None

    ext = file.name.split(".")[-1]
    path = f"{patient_id}/{uuid.uuid4()}.{ext}"
    bytes_data = file.read()

    supabase.storage.from_("patient-files").upload(path, bytes_data)

    supabase.table("patient_files").insert({
        "patient_id": patient_id,
        "file_name": path,
        "original_name": file.name,
        "uploaded_at": datetime.utcnow().isoformat()
    }).execute()

    return path


def get_patient_files(patient_id: str):
    res = supabase.table("patient_files").select("*").eq("patient_id", patient_id).execute()
    files = res.data or []

    for f in files:
        try:
            if isinstance(f.get("uploaded_at"), str):
                f["uploaded_at"] = datetime.fromisoformat(f["uploaded_at"])
        except:
            pass

    return files
