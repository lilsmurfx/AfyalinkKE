# pages/3_Patient_Dashboard.py
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.database import (
    get_patient_records,
    get_user_appointments,
    get_user_name,
    upload_patient_file,
    get_patient_files
)

st.set_page_config(page_title="Patient Dashboard", layout="wide")

# -----------------------
# Auth check
# -----------------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please login first.")
    st.stop()
if st.session_state.get("role") != "patient":
    st.error("Access denied. Patients only.")
    st.stop()

patient_id = st.session_state.get("user_id")
patient_name = get_user_name(patient_id)

st.title(f"Patient Dashboard — {patient_name}")
st.markdown("---")

# Fetch data
records = get_patient_records(patient_id) or []
appointments = get_user_appointments(patient_id, "patient") or []
files = get_patient_files(patient_id) or []

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Medical Records", len(records))
col2.metric("Appointments", len(appointments))
col3.metric("Files", len(files))

st.markdown("## Your Medical Records")
if records:
    df = pd.DataFrame(records)
    st.dataframe(df)
else:
    st.info("No medical records found.")

st.markdown("---")
st.header("Upload Documents (e.g., prescriptions, reports)")
upload_file = st.file_uploader("Choose a file to upload", type=["pdf", "png", "jpg", "jpeg"])
if upload_file and st.button("Upload Document"):
    try:
        path = upload_patient_file(patient_id, upload_file)
        st.success(f"Uploaded: {path}")
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Upload failed: {e}")

st.markdown("---")
st.header("Files Shared With You")
if files:
    # Show table with download links if bucket is public
    for f in files:
        uploaded_at = f.get("uploaded_at")
        if isinstance(uploaded_at, str):
            try:
                uploaded_at = datetime.fromisoformat(uploaded_at)
            except:
                pass
        st.write(f"- {f.get('original_name') or f.get('file_name')} — Uploaded: {uploaded_at}")
else:
    st.info("No files found.")

st.markdown("---")
st.header("Your Appointments")
if appointments:
    appt_df = pd.DataFrame(appointments)
    if "appointment_time" in appt_df.columns:
        def fmt(x):
            try:
                return x.strftime("%Y-%m-%d %H:%M") if hasattr(x, "strftime") else str(x)
            except:
                return str(x)
        appt_df["appointment_time"] = appt_df["appointment_time"].apply(fmt)
    st.dataframe(appt_df)
else:
    st.info("No appointments scheduled.")
