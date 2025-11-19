# utils/auth.py
# SIMPLE LOGIN SYSTEM (NO BCRYPT, NO JWT)
# Adds patient signup → also inserts into patients table

from datetime import datetime
from supabase_config import supabase
from utils.database import get_user_by_email


# -------------------------------------------------------
# SIMPLE PASSWORD CHECK (plain-text)
# -------------------------------------------------------
def verify_password(input_password: str, stored_password: str) -> bool:
    """
    Your Supabase database stores passwords in plain text (e.g., 'doctor3').
    So authentication uses direct string comparison.
    """
    if not stored_password:
        return False

    return input_password.strip() == str(stored_password).strip()


# -------------------------------------------------------
# SIGNUP (NOW CREATES ENTRY IN `patients` TABLE TOO)
# -------------------------------------------------------
def signup(email: str, password: str, role: str, full_name: str):
    # Check if user exists
    existing = get_user_by_email(email)
    if existing:
        return {"error": "User already exists."}

    clean_email = email.strip().lower()

    # Insert into USERS table
    res = supabase.table("users").insert({
        "email": clean_email,
        "password": password,   # stored as plain text (your current setup)
        "role": role,
        "full_name": full_name
    }).execute()

    if getattr(res, "error", None):
        return {"error": str(res.error)}

    # Retrieve new user's ID
    user_id = res.data[0].get("id")

    # If the user is a patient → also insert into PATIENTS table
    if role == "patient":
        supabase.table("patients").insert({
            "id": user_id,                     # SAME ID as in users table
            "doctor_id": None,                 # unassigned at signup
            "created_at": datetime.utcnow().isoformat()
        }).execute()

    return {
        "success": True,
        "message": "Signup successful. Please login.",
        "user_id": user_id
    }


# -------------------------------------------------------
# LOGIN
# -------------------------------------------------------
def login(email: str, password: str):
    clean_email = email.strip().lower()

    # Fetch user
    user = get_user_by_email(clean_email)

    if not user:
        return {"error": "Invalid email or password."}

    stored_pw = user.get("password", "")

    # Plain-text comparison
    if not verify_password(password, stored_pw):
        return {"error": "Invalid email or password."}

    # SUCCESS
    return {
        "success": True,
        "user": user,
        "role": user.get("role", "patient"),
        "access_token": None  # no JWT in this system
    }
