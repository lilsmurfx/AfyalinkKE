from utils.database import get_user_by_email

print("Doctor:", get_user_by_email("doctor3@afyalink.com"))
print("Admin:", get_user_by_email("admin-admin2@gmail.com"))
print("Patient:", get_user_by_email("patient2@gmail.com"))
