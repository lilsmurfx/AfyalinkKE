from supabase_config import supabase

def signup(email: str, password: str, role: str, full_name: str):
    if not email or not password:
        return {"error": "Email and password are required"}

    user = supabase.auth.sign_up({"email": email, "password": password})
    if user.user is None:
        return {"error": "Signup failed. Check email or password."}

    # Insert into users table
    supabase.table("users").insert({
        "id": user.user.id,
        "email": email,
        "role": role,
        "full_name": full_name
    }).execute()

    return {"success": True, "user_id": user.user.id}

def login(email: str, password: str):
    if not email or not password:
        return {"error": "Email and password are required"}

    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
    if res.user is None:
        return {"error": "Login failed or email not confirmed"}

    # Fetch role from users table
    user_data = supabase.table("users").select("*").eq("id", res.user.id).single().execute()
    if not user_data.data:
        return {"error": "User data not found"}

    return {"user": res.user, "role": user_data.data["role"]}
