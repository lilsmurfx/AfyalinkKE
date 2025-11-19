import streamlit as st
from utils.auth import login, signup
from utils.database import get_user_name

st.set_page_config(page_title="AfyaLink", layout="wide")

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


# --- Header ---
st.markdown(
    "<h1 style='text-align:center; color:#2C3E50;'>AfyaLink Medical System</h1>",
    unsafe_allow_html=True
)

st.markdown("<hr>", unsafe_allow_html=True)


<<<<<<< HEAD
card_style = """
    <div style='background-color:{bg}; padding:15px; border-radius:10px; text-align:center;'>
        <h4 style='color:white'>{role}</h4>
        <p style='color:white'>{info}</p>
    </div>
"""

with col1:
    if st.button("Login as Admin"):
        fill_demo("admin-admin2@gmail.com", "admin2")
    st.markdown(card_style.format(bg="#1abc9c", role="Admin",
                                  info="Email: admin-admin2@gmail.com<br>Password: admin2"), unsafe_allow_html=True)

with col2:
    if st.button("Login as Doctor"):
        fill_demo("doctor3@afyalink.com", "doctor3")
    st.markdown(card_style.format(bg="#3498db", role="Doctor",
                                  info="Email: doctor3@afyalink.com<br>Password: doctor3"), unsafe_allow_html=True)

with col3:
    if st.button("Login as Patient"):
        fill_demo("patient2@gmail.com", "patient2")
    st.markdown(card_style.format(bg="#e74c3c", role="Patient",
                                  info="Email: patient2@gmail.com<br>Password: patient2"), unsafe_allow_html=True)

# --- Logged Out State ---
=======
# =============================
# NOT LOGGED IN
# =============================
>>>>>>> 4b1e4db84cfe4b6df43b09d25cb3e296cd65e4d6
if not st.session_state["logged_in"]:

    tabs = st.tabs(["Login", "Sign Up"])

    # ---------------------------------------------------------
    # LOGIN TAB
    # ---------------------------------------------------------
    with tabs[0]:
        st.subheader("Login")

<<<<<<< HEAD
        # Autofill preserved
        email = st.text_input("Email", key="login_email", value=st.session_state["login_email"])
        password = st.text_input("Password", type="password", key="login_pass", value=st.session_state["login_pass"])
=======
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
>>>>>>> 4b1e4db84cfe4b6df43b09d25cb3e296cd65e4d6

        if st.button("Login"):
            res = login(email, password)

            # Login failed → show error
            if not res or res.get("error"):
                st.error(res.get("error", "Login failed. Check credentials."))
            
            elif not res.get("user"):
                st.error("Login failed: No user returned.")
            
            else:
                user = res["user"]

                # Store login info
                st.session_state["logged_in"] = True
<<<<<<< HEAD
                st.session_state["user_id"] = res["user"].id
                st.session_state["role"] = res["role"]
                st.session_state["full_name"] = get_user_name(res["user"].id)

                st.session_state["trigger_rerun"] = not st.session_state["trigger_rerun"]
                st.rerun()  # FIXED
=======
                st.session_state["user_id"] = user["id"]
                st.session_state["role"] = res.get("role", "patient")

                # Fetch full name if exists, else fallback
                st.session_state["full_name"] = user.get(
                    "user_metadata", {}
                ).get("full_name", "User")

                # No JWT for now
                st.session_state["access_token"] = None

                st.success("Login successful!")
                st.experimental_rerun()
>>>>>>> 4b1e4db84cfe4b6df43b09d25cb3e296cd65e4d6


    # ---------------------------------------------------------
    # SIGNUP TAB
    # ---------------------------------------------------------
    with tabs[1]:
        st.subheader("Sign Up")

        full_name = st.text_input("Full Name", key="signup_name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_pass")
        role = st.selectbox("Role", ["patient", "doctor"])

        if st.button("Sign Up"):
            res = signup(email, password, role, full_name)

            if res.get("error"):
                st.error(res["error"])
            else:
                st.success("Signup successful! Please login.")


# =============================
# LOGGED IN VIEW
# =============================
else:
    st.success(f"Welcome, {st.session_state.get('full_name', 'User')}!")
    st.info(f"You are logged in as: {st.session_state['role']}")
<<<<<<< HEAD
    st.info("Go to your dashboard from the left panel (Streamlit Pages).")

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user_id"] = None
        st.session_state["role"] = None
        st.session_state["full_name"] = None
        st.session_state["login_email"] = ""
        st.session_state["login_pass"] = ""
        st.session_state["trigger_rerun"] = not st.session_state["trigger_rerun"]
        st.rerun()  # FIXED
=======
    st.info("Use the left sidebar to navigate to your dashboard.")

    # Logout Button
    if st.button("Logout"):
        st.session_state.update({
            "logged_in": False,
            "user_id": None,
            "role": None,
            "full_name": None,
            "login_email": "",
            "login_pass": "",
            "access_token": None,
            "trigger_rerun": not st.session_state["trigger_rerun"]
        })
        st.experimental_rerun()
>>>>>>> 4b1e4db84cfe4b6df43b09d25cb3e296cd65e4d6
