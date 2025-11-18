from utils.auth import signup
from supabase_config import supabase

# Admin details
admin_email = "admin2@afyalink.com"
admin_password = "admin2"
admin_name = "Admin two"
admin_role = "admin"

# --- Step 1: Create the admin in Supabase Auth and users table ---
res = signup(admin_email, admin_password, admin_role, admin_name)

if "error" in res:
    print("Error creating admin:", res["error"])
else:
    print(f"Admin created successfully! User ID: {res['user_id']}")

    # --- Step 2 (optional, ensures admin exists in 'users' table) ---
    # Check if user exists in users table
    existing = supabase.table("users").select("*").eq("id", res["user_id"]).execute()
    if not existing.data:
        supabase.table("users").insert({
            "id": res["user_id"],
            "email": admin_email,
            "full_name": admin_name,
            "role": admin_role
        }).execute()
        print("Admin row added to users table.")
