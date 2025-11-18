import streamlit as st
import pandas as pd
from utils.database import (
    get_all_patients,
    get_doctor_patients,
    get_all_users,
    add_patient,
    get_user_name,
    unassign_patient,
)

# --- Access control ---
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please login first.")
    st.stop()
if st.session_state.get("role") != "admin":
    st.error("Access denied. Admins only.")
    st.stop()

st.set_page_config(page_title="Admin Dashboard", layout="wide")

user_id = st.session_state["user_id"]
user_name = get_user_name(user_id)

# --- Custom CSS ---
st.markdown("""
<style>
.header-bar {background-color: #1E3D59; padding: 15px; border-radius: 10px; color: white; font-size: 20px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;}
.logout-btn {background-color: #F2545B; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;}
.card {background: linear-gradient(135deg, #2E8B57, #1E3D59); color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px; transition: transform 0.2s;}
.card:hover {transform: scale(1.05);}
.card h1 {font-size: 36px; margin: 10px 0 0 0;}
.card h3 {font-size: 18px; margin: 0; opacity: 0.9;}
.section-title {font-weight: 700; font-size: 22px; color: #1E3D59; margin-top: 35px; margin-bottom: 15px;}
.unassign-btn {background-color: #d9534f !important; color: white !important; padding: 5px 12px !important; border-radius: 6px;}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown(f"""
<div class="header-bar">
    <div>👤 {user_name} | Role: Admin</div>
    <button class="logout-btn" onclick="window.location.reload();">Logout</button>
</div>
""", unsafe_allow_html=True)

st.title("🏥 AfyaLink Admin Dashboard")

# --- Fetch fresh data ---
users = get_all_users()
doctors = [u for u in users if u['role'] == 'doctor'] if users else []
patients = get_all_patients()

# --- Metrics ---
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="card"><h3>Total Doctors</h3><h1>{len(doctors)}</h1></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="card"><h3>Total Patients</h3><h1>{len(patients)}</h1></div>', unsafe_allow_html=True)
with col3:
    unassigned_patients = len([p for p in patients if not p['doctor_id']])
    st.markdown(f'<div class="card"><h3>Unassigned Patients</h3><h1>{unassigned_patients}</h1></div>', unsafe_allow_html=True)

# --- Doctors ---
st.markdown('<div class="section-title">👨‍⚕️ Doctors List</div>', unsafe_allow_html=True)
if doctors:
    doctors_df = pd.DataFrame(doctors)[['full_name', 'email']]
    st.dataframe(doctors_df, height=250)
else:
    st.info("No doctors found.")

# --- Patients ---
st.markdown('<div class="section-title">🧑‍🤝‍🧑 Patients List</div>', unsafe_allow_html=True)
if patients:
    patients_df = pd.DataFrame(patients)[['name', 'age', 'doctor_id']]
    st.dataframe(patients_df, height=250)
else:
    st.info("No patients found.")

# --- Add/Assign Patient ---
st.markdown('<div class="section-title">➕ Add / Assign Patient</div>', unsafe_allow_html=True)
with st.form("add_patient_form"):

    existing_patient_names = [p['name'] for p in patients] if patients else []
    patient_search = st.text_input("Search or Type New Patient Name")
    filtered_patients = [name for name in existing_patient_names if patient_search.lower() in name.lower()]
    
    patient_name = st.selectbox("Select Patient", options=[""] + filtered_patients)
    if not patient_name:
        patient_name = patient_search.strip()

    age = st.number_input("Age", min_value=0)

    doctor_map = {u['id']: u['full_name'] for u in doctors}
    doctor_search = st.text_input("Search Doctor")
    filtered_doctors = {id_: name for id_, name in doctor_map.items() if doctor_search.lower() in name.lower()}

    if filtered_doctors:
        selected_doctor_id = st.selectbox(
            "Assign to Doctor",
            options=list(filtered_doctors.keys()),
            format_func=lambda x: f"{filtered_doctors[x]}"
        )
    else:
        st.warning("No matching doctors found.")
        selected_doctor_id = None

    submitted = st.form_submit_button("Add / Assign Patient")
    if submitted:
        if not patient_name or not selected_doctor_id:
            st.error("Patient name and assigned doctor are required.")
        else:
            add_patient(patient_name, age, selected_doctor_id)
            st.success(f"Patient '{patient_name}' successfully assigned to {doctor_map[selected_doctor_id]}!")
            st.experimental_rerun()  # <-- refresh dashboard immediately

# --- Patients Under Doctor + DELETE BUTTON ---
st.markdown('<div class="section-title">🧹 Unassign / Remove Patient From Doctor</div>', unsafe_allow_html=True)

if doctors and patients:
    selected_doctor_view = st.selectbox(
        "Select Doctor",
        list(doctor_map.keys()),
        format_func=lambda x: doctor_map[x]
    )

    doctor_patients = get_doctor_patients(selected_doctor_view)

    if doctor_patients:
        st.write(f"### Patients under {doctor_map[selected_doctor_view]}")

        for p in doctor_patients:
            colA, colB, colC = st.columns([2, 2, 1])
            with colA:
                st.write(f"**{p['name']}**")
            with colB:
                st.write(f"Age: {p['age']}")
            with colC:
                if st.button("Unassign", key=f"del_{p['id']}"):
                    unassign_patient(p['id'])
                    st.success(f"Patient {p['name']} unassigned successfully!")
                    st.experimental_rerun()  # <-- refresh after unassign
    else:
        st.info("This doctor has no assigned patients.")
else:
    st.info("No doctors or patients available.")
