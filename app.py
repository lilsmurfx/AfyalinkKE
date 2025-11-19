# app.py
import streamlit as st
from utils.auth import login, signup
from utils.database import get_user_name

st.set_page_config(page_title="AfyaLink | Connected Healthcare", layout="wide")

# --- Initialize session state ---
default_state = {
    "logged_in": False,
    "trigger_rerun": False,
    "login_email": "",
    "login_pass": "",
    "user_id": None,
    "role": None,
    "full_name": None,
    "access_token": None
}

for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ======================================================================
# FULL THEME & PAGE STYLING
# ======================================================================
st.markdown(
    """
    <style>

    /* GLOBAL FONT */
    html, body, [class*="css"] {
        font-family: "Inter", sans-serif !important;
        color: #1F2937;
    }

    /* MAIN BACKGROUND */
    .reportview-container {
        background: linear-gradient(145deg, #eef2f3, #ffffff);
    }

    /* HERO SECTION */
    .hero-title {
        font-size: 52px;
        color: #0F172A;
        text-align: center;
        font-weight: 900;
        margin-top: 10px;
        letter-spacing: -1px;
    }

    .hero-sub {
        font-size: 22px;
        color: #475569;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 35px;
    }

    .hero-box {
        background: linear-gradient(135deg, #0ea5e9, #38bdf8, #7dd3fc);
        padding: 45px;
        border-radius: 18px;
        text-align: center;
        color: white;
        margin-bottom: 45px;
        box-shadow: 0px 12px 28px rgba(0,0,0,0.12);
    }

    /* FEATURES */
    .feature-card {
        background: white;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.07);
        text-align: center;
        transition: transform .25s ease, box-shadow .25s ease;
    }
    .feature-card:hover {
        transform: translateY(-6px);
        box-shadow: 0px 14px 30px rgba(0,0,0,0.12);
    }
    .feature-title {
        font-size: 20px;
        font-weight: 700;
        color: #0F172A;
        margin-top: 12px;
    }
    .feature-desc {
        font-size: 14px;
        color: #475569;
        margin-top: 4px;
    }

    /* LOGIN CARDS */
    .demo-card {
        background: #ffffff;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 14px;
    }

    /* TABS THEME */
    .stTabs [role="tab"] {
        background: #e2e8f0;
        border-radius: 7px;
        padding: 10px 18px;
        font-weight: 600;
        color: #1e293b;
    }
    .stTabs [aria-selected="true"] {
        background: #0ea5e9 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ======================================================================
# HERO SECTION
# ======================================================================
st.markdown("<div class='hero-title'>AfyaLink Medical Platform</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='hero-sub'>Connecting patients, doctors, and administrators in one seamless ecosystem.</div>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-box">
        <h2 style="margin-bottom: 0; font-weight:700;">Smart · Efficient · Integrated Healthcare</h2>
        <p style="margin-top: 10px; font-size:18px;">
            A next-generation digital health system enabling secure file sharing,
            real-time doctor-patient coordination, appointment scheduling,
            and centralized medical management.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ======================================================================
# FEATURES GRID
# ======================================================================
colA, colB, colC = st.columns(3)

with colA:
    st.markdown(
        """
        <div class='feature-card'>
            <img src='https://cdn-icons-png.flaticon.com/512/4320/4320355.png' width='64'>
            <div class='feature-title'>Smart Appointments</div>
            <div class='feature-desc'>Calendar-based scheduling with reminders and workflow automation.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with colB:
    st.markdown(
        """
        <div class='feature-card'>
            <img src='https://cdn-icons-png.flaticon.com/512/3209/3209265.png' width='64'>
            <div class='feature-title'>Secure Digital Records</div>
            <div class='feature-desc'>Encrypted document upload and instant doctor/patient access.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with colC:
    st.markdown(
        """
        <div class='feature-card'>
            <img src='https://cdn-icons-png.flaticon.com/512/1077/1077063.png' width='64'>
            <div class='feature-title'>Role-Based Dashboards</div>
            <div class='feature-desc'>Clean, powerful dashboards for admins, doctors, and patients.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")


# ======================================================================
# DEMO LOGIN BUTTONS
# ======================================================================
st.subheader("Quick Demo Accounts")

def fill_demo(email, password):
    st.session_state["login_email"] = email
    st.session_state["login_pass"] = password

demo_col1, demo_col2, demo_col3 = st.columns(3)

with demo_col1:
    if st.button("Admin Demo Login"):
        fill_demo("admin-admin2@gmail.com", "admin2")
    st.markdown("<div class='demo-card'>admin-admin2@gmail.com<br>admin2</div>", unsafe_allow_html=True)

with demo_col2:
    if st.button("Doctor Demo Login"):
        fill_demo("doctor3@afyalink.com", "doctor3")
    st.markdown("<div class='demo-card'>doctor3@afyalink.com<br>doctor3</div>", unsafe_allow_html=True)

with demo_col3:
    if st.button("Patient Demo Login"):
        fill_demo("patient2@gmail.com", "patient2")
    st.markdown("<div class='demo-card'>patient2@gmail.com<br>patient2</div>", unsafe_allow_html=True)

st.markdown("---")


# ======================================================================
# LOGIN / SIGNUP
# ======================================================================
if not st.session_state["logged_in"]:

    st.markdown("### Access the Platform")

    tabs = st.tabs(["Login", "Sign Up"])

    # LOGIN TAB
    with tabs[0]:

        email = st.text_input("Email", key="login_email", value=st.session_state["login_email"])
        password = st.text_input("Password", type="password", key="login_pass", value=st.session_state["login_pass"])

        if st.button("Login"):
            res = login(email, password)

            if res.get("error"):
                st.error(res["error"])
            else:
                user = res["user"]
                st.session_state["logged_in"] = True
                st.session_state["user_id"] = user.get("id")
                st.session_state["role"] = user.get("role")
                st.session_state["full_name"] = get_user_name(user.get("id"))
                st.experimental_rerun()

    # SIGNUP TAB
    with tabs[1]:

        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["patient", "doctor"])

        if st.button("Create Account"):
            res = signup(email, password, role, full_name)
            if res.get("error"):
                st.error(res["error"])
            else:
                st.success("Signup successful! You may now log in.")

else:
    st.success(f"Welcome, {st.session_state.get('full_name', 'User')}! 🎉")
    st.info(f"Logged in as **{st.session_state['role'].capitalize()}**.")

    if st.button("Logout"):
        st.session_state.update(default_state)
        st.experimental_rerun()
