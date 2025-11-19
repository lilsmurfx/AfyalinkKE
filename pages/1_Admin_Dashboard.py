# pages/1_Admin_Dashboard.py
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.database import (
    get_all_users,
    get_all_patients,
    get_user_name,
    get_patient_files,
    unassign_patient
)
from supabase_config import supabase

st.set_page_config(page_title="Admin Dashboard", layout="wide")

# -----------------------
# Access control
# -----------------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please login first.")
    st.stop()
if st.session_state.get("role") != "admin":
    st.error("Access denied. Admins only.")
    st.stop()

# -----------------------
# Header
# -----------------------
user_name = get_user_name(st.session_state.get("user_id"))
st.title(f"Admin Dashboard — {user_name}")
st.markdown("Manage users, assign/unassign patients to doctors, and inspect patient files.")
st.markdown("---")

# -----------------------
# Load users
# -----------------------
all_users = get_all_users() or []
doctors = [u for u in all_users if u.get("role") == "doctor"]
patients = [u for u in all_users if u.get("role") == "patient"]

# -----------------------
# Stats
# -----------------------
col1, col2, col3 = st.columns(3)
col1.metric("Total Doctors", len(doctors))
col2.metric("Total Patients", len(patients))

# Count unassigned patients
unassigned_count = (
    supabase.table("patients").select("*").is_("doctor_id", None).execute().data
)
col3.metric("Unassigned Patients", len(unassigned_count))

st.markdown("---")

# -----------------------
# Assign / Unassign Patients
# -----------------------
st.header("Assign or Unassign Patients")

# Build dropdown lists
patient_options = {
    f"{p.get('full_name') or p.get('email')} — {p.get('id')}": p.get("id")
    for p in patients
}

doctor_options = {
    f"{d.get('full_name') or d.get('email')} — {d.get('id')}": d.get("id")
    for d in doctors
}

col_p, col_d = st.columns(2)
with col_p:
    selected_patient_label = st.selectbox(
        "Select patient",
        ["Select..."] + list(patient_options.keys())
    )
with col_d:
    selected_doctor_label = st.selectbox(
        "Select doctor",
        ["Select..."] + list(doctor_options.keys())
    )

assign_col, unassign_col = st.columns(2)

# -----------------------
# ASSIGN PATIENT → DOCTOR (WITH DOCTOR NAME UPDATE)
# -----------------------
with assign_col:
    if st.button("Assign patient to doctor"):
        if selected_patient_label == "Select..." or selected_doctor_label == "Select...":
            st.error("Select both a patient and a doctor.")
        else:
            patient_id = patient_options[selected_patient_label]
            doctor_id = doctor_options[selected_doctor_label]

            # Fetch doctor name
            doctor_row = supabase.table("users").select("full_name").eq("id", doctor_id).single().execute()
            doctor_name = doctor_row.data.get("full_name", "Unknown Doctor")

            try:
                res = supabase.table("patients").update({
                    "doctor_id": doctor_id,
                    "doctor_name": doctor_name,
                    "updated_at": datetime.utcnow().isoformat()
                }).eq("id", patient_id).execute()

                if getattr(res, "error", None):
                    st.error(f"Assignment failed: {res.error}")
                else:
                    st.success(f"Assigned patient to Dr. {doctor_name}.")
                    st.experimental_rerun()

            except Exception as e:
                st.error(f"Assignment error: {e}")

# -----------------------
# UNASSIGN PATIENT
# -----------------------
with unassign_col:
    if st.button("Unassign patient from doctor"):
        if selected_patient_label == "Select...":
            st.error("Select a patient to unassign.")
        else:
            patient_id = patient_options[selected_patient_label]

            try:
                supabase.table("patients").update({
                    "doctor_id": None,
                    "doctor_name": None,
                    "updated_at": datetime.utcnow().isoformat()
                }).eq("id", patient_id).execute()

                st.success("Patient unassigned successfully.")
                st.experimental_rerun()

            except Exception as e:
                st.error(f"Unassign failed: {e}")

st.markdown("---")

# -----------------------
# Doctors Table
# -----------------------
st.header("Doctors")
if doctors:
    df = pd.DataFrame(doctors)

    # REMOVE PASSWORD COLUMN
    if "password" in df.columns:
        df = df.drop(columns=["password"])

    st.dataframe(df)
else:
    st.info("No doctors found.")

st.markdown("---")

# -----------------------
# Patients Table
# -----------------------
st.header("Patients")
if patients:
    dfp = pd.DataFrame(patients)

    # REMOVE PASSWORD COLUMN
    if "password" in dfp.columns:
        dfp = dfp.drop(columns=["password"])

    st.dataframe(dfp)
else:
    st.info("No patients found.")

st.markdown("---")

# -----------------------
# Patient File Inspection
# -----------------------
st.header("Inspect Patient Files")

if patient_options:
    inspect_label = st.selectbox(
        "Choose patient to view uploaded files",
        ["Select..."] + list(patient_options.keys()),
        key="inspect_patient"
    )

    if inspect_label != "Select...":
        pid = patient_options[inspect_label]

        try:
            files = get_patient_files(pid)
            if files:
                st.table(files)
            else:
                st.info("No files uploaded for this patient.")
        except Exception as e:
            st.error(f"Error fetching files: {e}")

else:
    st.info("No patients found.")
