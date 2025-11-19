import streamlit as st
import pandas as pd
import plotly.express as px
<<<<<<< HEAD
from datetime import datetime, timezone
from utils.database import (
    get_doctor_patients,
    add_record,
    get_user_appointments,
    add_appointment,
    get_user_name,
)
=======
from utils.database import (
    get_doctor_patients,
    get_user_appointments,
    get_user_name,
    upload_patient_file,
    get_patient_files
)
from supabase_config import supabase
from datetime import datetime
>>>>>>> 4b1e4db84cfe4b6df43b09d25cb3e296cd65e4d6

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

<<<<<<< HEAD
# --- Custom CSS ---
st.markdown(
    """
=======
# --- CSS ---
st.markdown("""
>>>>>>> 4b1e4db84cfe4b6df43b09d25cb3e296cd65e4d6
<style>
.metric-card { background-color: #2E8B57; color: white; border-radius: 12px; padding: 20px; text-align: center; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.2);}
.section-title { color: #2E8B57; font-weight: bold; font-size: 20px; margin-bottom: 10px;}
</style>
""",
    unsafe_allow_html=True,
)

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

<<<<<<< HEAD
# Logout button aligned right
logout_container = st.container()
with logout_container:
    logout_col1, logout_col2 = st.columns([9, 1])
    with logout_col2:
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

# ------------------------
# Fetch fresh data
# ------------------------
patients = get_doctor_patients(doctor_id) or []
appointments = get_user_appointments(doctor_id, "doctor") or []

# Normalize appointments: parse appointment_time to timezone-aware UTC
def parse_appointment_time(val):
    """
    Robustly parse an appointment_time value into a timezone-aware pandas.Timestamp (UTC).
    Accepts str, datetime, pandas.Timestamp.
    """
    try:
        return pd.to_datetime(val, utc=True)
    except Exception:
        # As fallback, try manual conversion
        try:
            if isinstance(val, datetime):
                if val.tzinfo is None:
                    return pd.to_datetime(val).tz_localize(timezone.utc)
                else:
                    return pd.to_datetime(val).tz_convert(timezone.utc)
        except Exception:
            return pd.NaT

for a in appointments:
    a_appt = parse_appointment_time(a.get("appointment_time"))
    # store back as ISO string or pandas.Timestamp depending on how your DB expects it.
    # For internal use we store the Timestamp object:
    a["appointment_time_parsed"] = a_appt

# ------------------------
# STAT CARDS
# ------------------------
total_patients = len(patients)
total_appointments = len(appointments)

now_utc = datetime.now(timezone.utc)

upcoming_appointments = (
    sum(
        1
        for a in appointments
        if a.get("appointment_time_parsed") is not pd.NaT
        and pd.notna(a.get("appointment_time_parsed"))
        and a["appointment_time_parsed"] > pd.Timestamp(now_utc)
    )
    if appointments
    else 0
)
=======
# --- Fetch Data ---
patients = get_doctor_patients(user_id)
appointments = get_user_appointments(user_id, "doctor")
patient_files = {p['id']: get_patient_files(p['id']) for p in patients} if patients else {}
>>>>>>> 4b1e4db84cfe4b6df43b09d25cb3e296cd65e4d6

# --- Metrics Cards ---
col1, col2, col3 = st.columns(3)
with col1:
<<<<<<< HEAD
    st.markdown(
        f"<div class='metric-card'><div style='font-size:34px;'>🧑‍🤝‍🧑</div><div style='font-size:28px;'>{total_patients}</div><div>Total Patients</div></div>",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"<div class='metric-card' style='background-color:#388E3C;'><div style='font-size:34px;'>📅</div><div style='font-size:28px;'>{total_appointments}</div><div>All Appointments</div></div>",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f"<div class='metric-card' style='background-color:#2E7D32;'><div style='font-size:34px;'>⏳</div><div style='font-size:28px;'>{upcoming_appointments}</div><div>Upcoming Appointments</div></div>",
        unsafe_allow_html=True,
    )

# ------------------------
# PATIENT LIST
# ------------------------
st.markdown("<div class='section-title'>🧑‍🤝‍🧑 Your Patients</div>", unsafe_allow_html=True)
with st.container():
    if patients:
        # Ensure consistent column names
        patient_df = pd.DataFrame(patients)
        # Safely handle missing columns
        display_cols = [c for c in ["id", "name", "age"] if c in patient_df.columns]
        st.dataframe(patient_df[display_cols], height=200)
    else:
        st.info("You have no assigned patients yet.")
=======
    st.markdown(f'<div class="metric-card">🧑‍🤝‍🧑<br>Total Patients<br><h2>{len(patients)}</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card">📅<br>Total Appointments<br><h2>{len(appointments)}</h2></div>', unsafe_allow_html=True)
with col3:
    next_appt_text = appointments[0]["appointment_time"].strftime("%d %b %Y %H:%M") if appointments else "No upcoming"
    st.markdown(f'<div class="metric-card">⏰<br>Next Appointment<br><h2>{next_appt_text}</h2></div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
>>>>>>> 4b1e4db84cfe4b6df43b09d25cb3e296cd65e4d6

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
<<<<<<< HEAD
                add_record(record_patient_id, title, description)
                st.success("Medical record added successfully!")
                st.rerun()  # reload dashboard to reflect new records

# ------------------------
# SCHEDULE APPOINTMENT
# ------------------------
st.markdown("<div class='section-title'>📅 Schedule Appointment</div>", unsafe_allow_html=True)
with st.container():
    if patients:
        # Build a mapping patient_name -> id (use unique names or show both if needed)
        patient_choices = {p.get("name", f"Patient {p.get('id')}"): p.get("id") for p in patients}
        with st.form("schedule_form"):
            patient_name = st.selectbox("Select Patient", list(patient_choices.keys()))
            appointment_patient_id = patient_choices.get(patient_name)
            # Use local date/time pickers; we'll convert to UTC-aware datetime before saving
            date_selected = st.date_input("Select Date", datetime.now().date())
            time_selected = st.time_input("Select Time", datetime.now().time())
            submitted_appointment = st.form_submit_button("Schedule")
            if submitted_appointment:
                # Combine into naive datetime, then make timezone-aware in UTC
                appt_naive = datetime.combine(date_selected, time_selected)
                appt_aware_utc = appt_naive.replace(tzinfo=timezone.utc)
                # Persist using the expected format (datetime or ISO string) - using datetime object here
                add_appointment(doctor_id, appointment_patient_id, appt_aware_utc)
                st.success(f"Appointment scheduled for {patient_name} on {appt_aware_utc.isoformat()}")
                st.rerun()  # reload dashboard to show new appointment
    else:
        st.warning("You have no patients to schedule appointments for.")

# ------------------------
# APPOINTMENTS CALENDAR
# ------------------------
st.markdown("<div class='section-title'>📊 Appointments Calendar</div>", unsafe_allow_html=True)
appointments = get_user_appointments(doctor_id, "doctor") or []

# Build dataframe safely and normalize times to UTC-aware timestamps
if appointments:
    df = pd.DataFrame(appointments)

    # If appointment_time_parsed exists from earlier normalization, prefer it
    if "appointment_time_parsed" in df.columns:
        df["appointment_time"] = df["appointment_time_parsed"]
    else:
        df["appointment_time"] = pd.to_datetime(df["appointment_time"], utc=True)

    # Drop rows with invalid times
    df = df[pd.notna(df["appointment_time"])].copy()

    # Map patient ids to names
    patient_map = {p.get("id"): p.get("name", f"Patient {p.get('id')}") for p in patients}
    # For safety, also map string version of id
    patient_map_str = {str(k): v for k, v in patient_map.items()}
    df["patient_name"] = df["patient_id"].map(patient_map).fillna(df["patient_id"].map(patient_map_str)).fillna("Unknown")

    # Prepare plotting fields
    df["date"] = df["appointment_time"].dt.date
    df["hour"] = df["appointment_time"].dt.hour

    fig = px.scatter(
        df,
        x="hour",
        y="date",
        color="patient_name",
        hover_data=["status", "patient_id", "appointment_time"],
        labels={"hour": "Hour of Day", "date": "Date"},
        title="Appointments Overview",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), height=600)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No scheduled appointments yet.")
=======
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
>>>>>>> 4b1e4db84cfe4b6df43b09d25cb3e296cd65e4d6
