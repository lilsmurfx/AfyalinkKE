import streamlit as st
import pandas as pd
from datetime import datetime, time, date, timedelta
from utils.database import (
    get_doctor_patients,
    get_user_appointments,
    get_user_name,
    upload_patient_file,
    add_appointment
)
from supabase_config import supabase
from streamlit_calendar import calendar


st.set_page_config(page_title="Doctor Dashboard", layout="wide")

# -----------------------
# ACCESS CONTROL
# -----------------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please login first.")
    st.stop()

if st.session_state.get("role") != "doctor":
    st.error("Access denied — doctors only.")
    st.stop()

doctor_id = st.session_state.get("user_id")
doctor_name = get_user_name(doctor_id)

st.title(f"Doctor Dashboard — Dr. {doctor_name}")
st.markdown("Manage your patients, appointments, medical documents, and schedule.")
st.markdown("---")


# -----------------------
# FETCH DATA
# -----------------------
patients = get_doctor_patients(doctor_id) or []
appointments = get_user_appointments(doctor_id, "doctor") or []

# Build safe patient lookup
patient_lookup = {
    str(p.get("id")): (
        p.get("full_name")
        or p.get("name")
        or p.get("email")
        or "Unknown Patient"
    )
    for p in patients
}

# -----------------------
# METRICS
# -----------------------
total_appts = len(appointments)
pending_appts = len([a for a in appointments if (a.get("status") or "").lower() in ["scheduled", "pending"]])
completed_appts = len([a for a in appointments if (a.get("status") or "").lower() in ["completed", "done"]])

c1, c2, c3 = st.columns(3)
c1.metric("Total Appointments", total_appts)
c2.metric("Pending", pending_appts)
c3.metric("Completed", completed_appts)

st.markdown("---")


# -----------------------
# PATIENT LIST
# -----------------------
st.header("Your Patients")

if patients:
    df_pat = pd.DataFrame(patients)
    cols = [c for c in ["id", "full_name", "email", "created_at"] if c in df_pat.columns]
    st.dataframe(df_pat[cols])
else:
    st.info("No patients currently assigned to you.")

st.markdown("---")


# -----------------------
# CREATE APPOINTMENT
# -----------------------
st.header("Create Appointment")

if patients:
    patient_options = ["-- Select patient --"] + list(patient_lookup.keys())

    selected_patient_key = st.selectbox(
        "Select patient",
        patient_options,
        format_func=lambda k: patient_lookup.get(k, "") if k != "-- Select patient --" else "",
        key="appointment_patient_select"
    )
    selected_patient_id = None if selected_patient_key == "-- Select patient --" else selected_patient_key

    appt_date = st.date_input("Appointment Date", value=date.today())
    appt_time = st.time_input("Appointment Time", value=time(10, 0))

    if st.button("Create Appointment", key="create_appt_submit"):
        if not selected_patient_id:
            st.error("Please select a patient.")
        else:
            appt_dt = datetime.combine(appt_date, appt_time)
            try:
                add_appointment(doctor_id, selected_patient_id, appt_dt)
                st.success("Appointment created successfully.")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error creating appointment: {e}")
else:
    st.info("No patients to create appointments for.")

st.markdown("---")


# -----------------------
# UPLOAD FILE
# -----------------------
st.header("Upload Patient Document")

if patients:
    upload_options = ["-- Select patient --"] + list(patient_lookup.keys())

    upload_key = st.selectbox(
        "Select Patient",
        upload_options,
        format_func=lambda k: patient_lookup.get(k, "") if k != "-- Select patient --" else "",
        key="file_upload_patient_select"
    )
    upload_patient_id = None if upload_key == "-- Select patient --" else upload_key

    upload_file = st.file_uploader("Choose file", type=["pdf", "jpg", "jpeg", "png"])

    if st.button("Upload File", key="upload_file_btn"):
        if not upload_patient_id:
            st.error("Please select a patient first.")
        elif not upload_file:
            st.error("Please choose a file to upload.")
        else:
            try:
                path = upload_patient_file(upload_patient_id, upload_file)
                st.success(f"File uploaded successfully: {path}")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Upload failed: {e}")
else:
    st.info("No patients to upload documents for.")

st.markdown("---")


# -----------------------
# DELETE A SCHEDULED APPOINTMENT
# -----------------------
def delete_appointment(appt_id: str):
    try:
        supabase.table("appointments").delete().eq("id", appt_id).execute()
        return True
    except:
        return False


# -----------------------
# APPOINTMENTS TABLE
# -----------------------
st.header("Appointments Overview")

if appointments:
    df = pd.DataFrame(appointments)

    # Add patient names
    df["patient_name"] = df["patient_id"].apply(lambda x: patient_lookup.get(str(x), "Unknown"))

    # Format timestamps
    df["appointment_time"] = df["appointment_time"].apply(
        lambda t: t.strftime("%Y-%m-%d %H:%M") if hasattr(t, "strftime") else str(t)
    )

    st.subheader("All Appointments")

    for i, row in df.iterrows():
        with st.container():
            cA, cB, cC, cD = st.columns([4, 3, 3, 1])

            cA.write(f"📅 **{row['appointment_time']}**")
            cB.write(f"👤 {row['patient_name']}")
            cC.write(f"Status: **{row.get('status', 'scheduled')}**")

            if cD.button("❌ Remove", key=f"del_{row['id']}"):
                if delete_appointment(row["id"]):
                    st.success("Appointment removed.")
                    st.experimental_rerun()
                else:
                    st.error("Error removing appointment.")

else:
    st.info("No scheduled appointments.")

st.markdown("---")


# -----------------------
# CALENDAR VIEW
# -----------------------
st.header("Appointment Calendar")

events = []
for a in appointments:
    t = a.get("appointment_time")

    # Convert string → datetime
    if isinstance(t, str):
        try:
            t = datetime.fromisoformat(t)
        except:
            continue

    if not t:
        continue

    events.append({
        "title": patient_lookup.get(str(a.get("patient_id")), "Unknown"),
        "start": t.strftime("%Y-%m-%dT%H:%M:%S"),
        "end": (t + timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M:%S")
    })

calendar(
    events=events,
    options={
        "initialView": "dayGridMonth",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay"
        }
    }
)
