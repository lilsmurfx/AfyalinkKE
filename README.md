# 🌐 AfyaLink — Connected Healthcare Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![Supabase](https://img.shields.io/badge/Backend-Supabase-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

> **AfyaLink** is a modern, cloud-native healthcare coordination system that connects **patients**, **doctors**, and **administrators** into a single, secure digital ecosystem. Manage appointments, share medical documents, assign patients to doctors, and operate role-based dashboards — all powered by Streamlit and Supabase.

---

## 🚀 Live demo & GitHub Pages
- **Streamlit app (deploy your own)**: run locally or deploy to Streamlit Cloud  
- **Landing page (GitHub Pages)**: `/docs/index.html` — (enable Pages for `main/docs` if needed)

---

## ✨ Key Features

- Role-based dashboards (Admin / Doctor / Patient)  
- Appointment scheduling + calendar view  
- Secure file uploads and patient document manager  
- Admin: view users, assign/unassign patients, inspect patient files  
- Demo accounts for quick testing  
- Clean investor-ready UI and documentation

---

AfyaLink/
│
├── app.py # Landing page + login/signup
├── requirements.txt # Python dependencies
├── README.md # This file
├── LICENSE # MIT License
├── .gitignore
├── supabase_config.py # Supabase connection (local)
│
├── utils/
│ ├── auth.py # Authentication & signup (simple mode)
│ └── database.py # Supabase DB helpers (patients, appointments, files)
│
├── pages/
│ ├── 1_Admin_Dashboard.py
│ ├── 2_Doctor_Dashboard.py
│ └── 3_Patient_Dashboard.py
│
├── docs/
│ └── index.html # GitHub Pages landing page
│
└── .github/
└── workflows/
└── deploy.yml # GitHub Actions workflow (CI / deployment scaffold)



---

## ✅ Demo Accounts (for testing)
Use these demo credentials to quickly explore the app:

| Role     | Email                    | Password |
|----------|--------------------------|----------|
| Admin    | admin-admin2@gmail.com   | admin2   |
| Doctor   | doctor3@afyalink.com     | doctor3  |
| Patient  | patient2@gmail.com       | patient2 |

> These credentials correspond to plain-text passwords in the demo setup. For production, **replace with hashed passwords and secure JWT/OAuth flows**.

---

## 🔧 Installation (Local)

1. Clone repository:
```bash
git clone https://github.com/lilsmurfx/AfyalinkKE.git
cd AfyalinkKE

Create and activate a virtual environment (recommended):

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Configure Supabase keys (see Secrets below).

Run the app:

streamlit run app.py


🔐 Secrets & Configuration

Create a .streamlit/secrets.toml file or set environment variables for local development:

Example secrets.toml
# .streamlit/secrets.toml
SUPABASE_URL = "https://<your-supabase-project>.supabase.co"
SUPABASE_KEY = "<your-anon-or-service-key>"

Important: Never commit secrets.toml or any API keys to source control. Use GitHub Secrets or Streamlit Cloud secrets for deployment.

🗄 Database / Schema Overview (Supabase)

Recommended tables (example):

users

id (UUID), email, password, role (admin/doctor/patient), full_name, created_at

patients

id (UUID - same as users.id), doctor_id (UUID), doctor_name, created_at

appointments

id, doctor_id, patient_id, appointment_time (timestamp), status, created_at

medical_records / patient_files

id, patient_id, file_name, original_name, uploaded_at

Adjust column names to match the code; the provided utilities expect these fields.

☁️ Deployment
Streamlit Cloud

Push your repo to GitHub (main branch).

Create a new app on Streamlit Cloud and connect it to your repo.

Set secrets in Streamlit Cloud (SUPABASE_URL and SUPABASE_KEY).
Streamlit auto-deploys on pushes to the connected branch.

GitHub Actions (CI)

A lightweight workflow is included in .github/workflows/deploy.yml to run checks and install dependencies. Streamlit Cloud redeploys automatically when GitHub updates.

📁 GitHub Pages (Landing Page)

A simple landing page is in docs/index.html. To publish:

Go to GitHub repo Settings → Pages → Source: main / docs folder → Save.

🧪 Tests & Validation (suggested)

Validate DB connectivity and RLS policies in Supabase.

Test file upload limits and storage permissions.

Confirm appointment timezone handling.

Add unit tests for critical logic (auth, DB helpers).

🔒 Security Notes (Important)

Current demo uses plain-text passwords for ease of testing. Do not use plain-text passwords in production.

For production:

Use bcrypt/argon2 for password hashing.

Implement JWT or OAuth2 access tokens.

Secure Supabase service keys on the server side.

Ensure RLS policies and bucket permissions are correct.

📈 Roadmap & Monetization Ideas

Mobile apps (React Native)

AI-assisted triage & clinical decision support

Clinic/hospital B2B subscriptions

Enterprise integrations (EMR/EHR connectors)

Insurance & billing modules

🧑‍💻 Contribution

Contributions are welcome. Please open issues or pull requests. Suggested workflow:

Fork repo

Create feature branch

Add tests & documentation

Submit PR

📄 License

This project is released under the MIT License. See the LICENSE file for details.

📞 Contact / Author

Developer: lilsmurfx

Repo: https://github.com/lilsmurfx/AfyalinkKE

📝 Short Investor Pitch (elevator)

AfyaLink solves fragmentation in healthcare by providing a single cloud-native platform for appointments, secure document exchange, and role-based workflows. It’s designed for fast deployment to clinics and scalable integration with hospitals, with multiple revenue opportunities: SaaS subscriptions, enterprise licensing, and value-added AI features. Early demos show reduced admin overhead and faster patient–doctor coordination.



## 🧭 Repo structure

