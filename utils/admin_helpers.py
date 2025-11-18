# utils/admin_helpers.py
from supabase_config import supabase

def create_user_account(email: str, password: str, full_name: str, role: str):
    """
    Create a new user in Supabase Auth and add to the users table.
    Roles: 'admin', 'doctor', 'patient'
    """
    # 1️⃣ Create in Supabase Auth
    auth_res = supabase.auth.sign_up({
        "email": email,
        "password": password
    })

    if auth_res.user is None:
        return {"error": "Failed to create user in Supabase Auth."}

    user_id = auth_res.user.id

    # 2️⃣ Insert into users table
    res = supabase.table("users").insert({
        "id": user_id,
        "email": email,
        "full_name": full_name,
        "role": role
    }).execute()

    if res.error:
        return {"error": f"Failed to insert user into users table: {res.error}"}

    return {"success": True, "user_id": user_id}
