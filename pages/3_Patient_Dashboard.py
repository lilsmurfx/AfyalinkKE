import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database import get_patient_records, get_user_appointments, get_user_name

# --- Access control ---
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please login first.")
    st.stop()
if st.session_state.get("role") != "patient":
    st.error("Access denied. Patients only.")
    st.stop()

st.set_page_config(page_title="Patient Dashboard", layout="wide")

user_id = st.session_state["user_id"]
user_name = get_user_name(user_id)

# --- Custom CSS for cards and sections ---
st.markdown("""
<style>
.card {
    background-color: #F5F5F5;  /* Admin dashboard card color */
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.metric-card {
    background-color: #2E8B57;  /* Admin dashboard green theme */
    color: white;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    font-weight: bold;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
}
.section-title {
    color: #2E8B57;
    font-weight: bold;
    font-size: 20px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- Header Bar ---
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
    <div>👤 {user_name} | Role: Patient</div>
    <div><button onclick="window.location.reload();">Logout</button></div>
</div>
""", unsafe_allow_html=True)

# --- Fetch Data ---
records = get_patient_records(user_id)
appointments = get_user_appointments(user_id, "patient")

# --- Metrics Cards ---
total_visits = len(records)
total_appointments = len(appointments)
upcoming_appt = pd.to_datetime(appointments[0]['appointment_time']) if appointments else None

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-card">🩺<br>Total Visits<br><h2>{total_visits}</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card">📅<br>Total Appointments<br><h2>{total_appointments}</h2></div>', unsafe_allow_html=True)
with col3:
    next_appt_text = upcoming_appt.strftime("%d %b %Y %H:%M") if upcoming_appt else "No upcoming"
    st.markdown(f'<div class="metric-card">⏰<br>Next Appointment<br><h2>{next_appt_text}</h2></div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# --- Medical Records Section ---
st.markdown('<div class="section-title">📄 Your Medical Records</div>', unsafe_allow_html=True)
if records:
    record_df = pd.DataFrame(records)
    search = st.text_input("Search Records by Title")
    filtered_records = record_df[record_df['record_title'].str.contains(search, case=False)] if search else record_df
    st.dataframe(filtered_records[['record_title', 'description']], height=250)
    csv = filtered_records.to_csv(index=False).encode('utf-8')
    st.download_button("Download Records as CSV", csv, "medical_records.csv", "text/csv")
else:
    st.info("No medical records found.")

st.markdown("<hr>", unsafe_allow_html=True)

# --- Appointments Section ---
st.markdown('<div class="section-title">📅 Your Appointments</div>', unsafe_allow_html=True)
if appointments:
    appt_df = pd.DataFrame(appointments)
    appt_df['appointment_time'] = pd.to_datetime(appt_df['appointment_time'])
    appt_df = appt_df.sort_values('appointment_time')
    st.dataframe(appt_df[['appointment_time', 'status']], height=250)

    # Appointments chart
    appt_df['month'] = appt_df['appointment_time'].dt.to_period('M')
    monthly_count = appt_df.groupby('month').size().reset_index(name='count')
    fig = px.bar(monthly_count, x='month', y='count', title="Appointments per Month",
                 text='count', color_discrete_sequence=['#2E8B57'])
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No scheduled appointments.")

st.markdown("<hr>", unsafe_allow_html=True)

# --- Upload Lab Reports Section ---
st.markdown('<div class="section-title">🧾 Upload Lab Reports / Prescriptions</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "png", "jpg", "jpeg"])
if uploaded_file:
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
