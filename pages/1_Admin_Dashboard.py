import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database import (
    get_doctor_patients,
    get_user_appointments,
    get_user_name,
    upload_patient_file,
    get_patient_files
)
from supabase_config import supabase
from datetime import datetime

# --- Access control ---
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please login first.")
    st.stop()
if st.session_state.get("role") != "doctor":
    st.error("Access denied. Doctors only.")
    st.stop()

st.set_page_config(page_title="Doctor Dashboard", layout="wide")

# --- User info ---
user_id = st.session_state["user_id"]          # Supabase Auth UID
user_token = st.session_state.get("access_token")  # Supabase JWT
user_name = get_user_name(user_id)

# --- CSS ---
st.markdown("""
<style>
.metric-card { background-color: #2E8B57; color: white; border-radius: 12px; padding: 20px; text-align: center; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.2);}
.section-title { color: #2E8B57; font-weight: bold; font-size: 20px; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown(f"""
<div style="
    background-color: #2E8B57; 
    padding: 12px; 
    border-radius: 12px; 
    color: white; 
    font-size: 20px;
    display: flex; 
    justify-content: space-between;
    align-items: center;">
    <div>👨‍⚕️ Dr. {user_name} | Role: Doctor</div>
    <div><button onclick="window.location.reload();">Logout</button></div>
</div>
""", unsafe_allow_html=True)

# --- Fetch Data ---
patients = get_doctor_patients(user_id)
appointments = get_user_appointments(user_id, "doctor")
patient_files = {p['id']: get_patient_files(p['id']) for p in patients} if patients else {}

# --- Metrics Cards ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-card">🧑‍🤝‍🧑<br>Total Patients<br><h2>{len(patients)}</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card">📅<br>Total Appointments<br><h2>{len(appointments)}</h2></div>', unsafe_allow_html=True)
with col3:
    next_appt_text = appointments[0]["appointment_time"].strftime("%d %b %Y %H:%M") if appointments else "No upcoming"
    st.markdown(f'<div class="metric-card">⏰<br>Next Appointment<br><h2>{next_appt_text}</h2></div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# --- Patients Table ---
st.markdown('<div class="section-title">🧑‍🤝‍🧑 Your Patients</div>', unsafe_allow_html=True)
if patients:
    patients_df = pd.DataFrame(patients)[['name', 'age']]
    st.dataframe(patients_df, height=250)
else:
    st.info("No patients assigned yet.")

# --- Upload Files for a Patient ---
st.markdown('<div class="section-title">🧾 Upload Files for a Patient</div>', unsafe_allow_html=True)
if patients:
    selected_patient_id = st.selectbox(
        "Select Patient",
        [p['id'] for p in patients],
        format_func=lambda x: next(p['name'] for p in patients if p['id'] == x)
    )

    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "png", "jpg", "jpeg"])
    if uploaded_file:
        try:
            if not user_token:
                st.error("User token missing. Please login again.")
            else:
                upload_patient_file(selected_patient_id, uploaded_file, user_token)
                st.success(f"File '{uploaded_file.name}' uploaded successfully!")
                st.experimental_rerun()
        except Exception as e:
            st.error(f"Upload failed: {e}")
else:
    st.info("No patients available for file uploads.")

# --- Patient Files ---
st.markdown('<div class="section-title">📂 Patient Files</div>', unsafe_allow_html=True)
if patients and patient_files:
    for pid, files in patient_files.items():
        patient_name = next(p['name'] for p in patients if p['id'] == pid)
        st.write(f"### Files for {patient_name}")
        if files:
            for f in files:
                uploaded_at_text = f['uploaded_at'].strftime('%d %b %Y %H:%M') if isinstance(f['uploaded_at'], datetime) else str(f['uploaded_at'])
                st.write(f"- {f['original_name']} (Uploaded: {uploaded_at_text})")
                url = supabase.storage.from_('patient-files').get_public_url(f['file_name'])['public_url']
                st.markdown(f"[Download]({url})")
        else:
            st.info("No files uploaded yet.")
else:
    st.info("No patient files available.")

# --- Appointments Table ---
st.markdown('<div class="section-title">📅 Your Appointments</div>', unsafe_allow_html=True)
if appointments:
    appt_df = pd.DataFrame(appointments).sort_values('appointment_time')
    st.dataframe(appt_df[['patient_id', 'appointment_time', 'status']], height=250)
    
    # Chart appointments per month
    appt_df['month'] = appt_df['appointment_time'].dt.to_period('M')
    monthly_count = appt_df.groupby('month').size().reset_index(name='count')
    fig = px.bar(monthly_count, x='month', y='count', title="Appointments per Month", text='count', color_discrete_sequence=['#2E8B57'])
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No scheduled appointments.")
