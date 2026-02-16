from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import Max
from .utils import send_appointment_email




from Patients.models import Patients

from appointments.models import Appointment

def home(request):
    user = None
    if 'user_id' in request.session:
        try:
            user = Patients.objects.get(id=request.session['user_id'])
        except Patients.DoesNotExist:
            request.session.flush()

    return render(request, 'index.html', {"logged_user": user})



def loginpage(request):
    return render(request,'login.html')

def signinpage(request):
    return render(request,'signup.html')


def patient_dashboard(request):
    return render(request, 'patient.html')

def doctor_dashboard(request):
    if 'user_id' not in request.session:
        return redirect('loginpage')
    if request.session.get('role', '').lower() != 'doctor':
        return redirect('loginpage')
    return render(request, 'doctor.html')


def reception_dashboard(request):
    return render(request, 'reception.html')


def logout_view(request):
    request.session.flush() 
    return redirect('loginpage')  


def blood_bank(request):
    return render(request,'blood_bank.html')


from Doctors.models import Doctor

def appointment(request):
     doctors = Doctor.objects.all()
     print("DOCTORS:", doctors.count())
     return render(request,'book_appointment.html',{'doctors': doctors})

from django.shortcuts import get_object_or_404


def doctor_appointments(request):
    if request.session.get("role", "").lower() != "doctor":
        return redirect("loginpage")

    doctor_id = request.session.get("doctor_id")
    if not doctor_id:
        return redirect("loginpage")

    doctor = get_object_or_404(Doctor, id=doctor_id)

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).select_related("patient").order_by("-date", "-time")

    return render(request, "doctor_appointments.html", {"appointments": appointments})



from django.db import transaction
@transaction.atomic


def update_appointment_status(request, appointment_id):
    # ✅ allow only doctors
    if request.session.get("role", "").lower() != "doctor":
        return redirect("loginpage")

    doctor_id = request.session.get("doctor_id")
    if not doctor_id:
        return redirect("loginpage")

    doctor = get_object_or_404(Doctor, id=doctor_id)

    # ✅ lock + ensure doctor updates only their own appointment
    appointment = get_object_or_404(
        Appointment.objects.select_for_update(),
        id=appointment_id,
        doctor=doctor
    )

    if request.method == "POST":
        action = request.POST.get("action")  # "approved" or "rejected"

        if action == "approved":
            appointment.status = "approved"
            appointment.rejection_reason = None

            # ✅ generate token ONLY when approved (and only once)
            if appointment.token_number is None:
                last_token = (
                    Appointment.objects
                    .select_for_update()
                    .filter(
                        doctor=doctor,
                        date=appointment.date,
                        status__in=["approved", "done"],
                        token_number__isnull=False
                    )
                    .aggregate(mx=Max("token_number"))["mx"] or 0
                )
                appointment.token_number = last_token + 1

            appointment.save()

            # ✅ ADDED: send email to patient after approval
            current_token = 0  # (aapke system me current token track nahi ho raha)
            people_ahead = max((appointment.token_number or 0) - current_token - 1, 0)
            wait_minutes = people_ahead * 10  # 10 min per patient (change if you want)

            # ensure patient email exists: appointment.patient.email
            send_appointment_email(appointment, people_ahead, wait_minutes)

        elif action == "rejected":
            appointment.status = "rejected"
            appointment.rejection_reason = request.POST.get("reason", "Doctor unavailable")
            appointment.token_number = None  # ✅ optional: ensure no token for rejected
            appointment.save()

    return redirect("doctor_appointments")


def buy_blood(request,blood_group):
    pass