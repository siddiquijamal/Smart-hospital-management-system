from django.core.mail import send_mail
from django.conf import settings

def _patient_display_name(patient) -> str:
    """
    Patient ka best possible name return karo.
    Agar name field nahi hai to other fields se fallback.
    """
    for field in ("name", "full_name", "patient_name", "username", "first_name"):
        val = getattr(patient, field, None)
        if val:
            return str(val)
    email = getattr(patient, "email", "") or ""
    return email.split("@")[0] if "@" in email else "Patient"

def send_appointment_email(appointment, people_ahead, wait_minutes):
    subject = "Appointment Approved ✅ | Token Details"

    token_number = getattr(appointment, "token_number", "N/A")
    current_token = getattr(appointment, "current_token", 0)

    hospital_name = "HMS Hospital"
    hospital_address = "Andheri East, Mumbai, Maharashtra – 400069"
    hospital_contact = "+91 98765 43210"

    patient = appointment.patient
    patient_name = _patient_display_name(patient)

    message = f"""Dear {patient_name},

We are pleased to inform you that your appointment has been approved successfully ✅

🏥 Hospital Details
Hospital Name : {hospital_name}
Address       : {hospital_address}
Contact       : {hospital_contact}

👨‍⚕️ Doctor Information
Doctor        : Dr. {appointment.doctor}
Date          : {appointment.date}
Time          : {appointment.time}

🎟 Token Information
Your Token No : {token_number}
Current Token : {current_token}

👥 Patients Ahead of You : {people_ahead}
⏳ Estimated Waiting Time : ~{wait_minutes} minutes

✨ Kindly arrive 10 minutes early to ensure a smooth check-in.
We look forward to welcoming you. Wishing you a comfortable visit!

Warm regards,  
{hospital_name}
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [patient.email],
        fail_silently=False
    )
