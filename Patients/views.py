from django.shortcuts import render, redirect
from .models import Patients
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Max



def signindetail(request):
    if request.method == "POST":
        fullname = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'signup.html', {
                'error': 'Passwords do not match'
            })

        Patients.objects.create(
            fullname=fullname,
            email=email,
            phone=phone,
            role=role,
            password=make_password(password)

        )

        return redirect('loginpage')  # ✅ redirect after POST

    return render(request, 'signup.html')

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from Patients.models import Patients
from Doctors.models import Doctor

def logindetail(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Patients.objects.get(email=email)

            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['role'] = user.role
                request.session['email'] = user.email

                role = (user.role or "").lower()

                if role == 'doctor':
                    # ✅ find the doctor record (NO password check)
                    doctor = Doctor.objects.filter(email=user.email).first()
                    if not doctor:
                        return render(request, 'login.html', {
                            'error': 'Doctor profile not found. Add this doctor in Doctor table.'
                        })

                    request.session['doctor_id'] = doctor.id
                    return redirect('doctor_appointments')

                elif role == 'receptionist':
                    return redirect('reception_dashboard')

                return redirect('patient_dashboard')

            return render(request, 'login.html', {'error': 'Invalid password'})

        except Patients.DoesNotExist:
            return render(request, 'login.html', {'error': 'Email not registered'})

    return render(request, 'login.html')


from django.shortcuts import render, redirect
from Patients.models import Patients
from appointments.models import Appointment 

def patient_appointments_page(request):
    # 1) check login via session
    if 'user_id' not in request.session:
        return redirect('loginpage')

    # 2) get patient object
    patient = Patients.objects.get(id=request.session['user_id'])

    # 3) fetch only this patient's appointments
    appointments = (
        Appointment.objects
        .filter(patient=patient)
        .select_related('doctor')
        .order_by('-date', '-time')
    )

    # 4) stats for the modern page
    total = appointments.count()
    pending = appointments.filter(status='pending').count()
    approved = appointments.filter(status='approved').count()
    rejected = appointments.filter(status='rejected').count()

    context = {
        "patient": patient,
        "appointments": appointments,
        "total": total,
        "pending": pending,
        "approved": approved,
        "rejected": rejected,
    }
    return render(request, "patient.html", context)






from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from appointments.models import Appointment
from Doctors.models import Doctor
from Patients.models import Patients


def track_token(request, appointment_id):
    if 'user_id' not in request.session:
        return redirect('loginpage')

    patient = Patients.objects.get(id=request.session["user_id"])
    appt = get_object_or_404(Appointment, id=appointment_id, patient=patient)

    doctor = appt.doctor
    now_token = doctor.current_token or 0   # ✅ if None -> 0

    # ✅ if token not set yet, avoid math crash
    if appt.token_number is None:
        return render(request, "track_token.html", {
            "appt": appt,
            "doctor": doctor,
            "now_token": now_token,
            "people_ahead": 0,
            "est_minutes": 0,
            "error": "Token not generated for this appointment yet."
        })

    if now_token == 0:
        people_ahead = appt.token_number - 1
    else:
        people_ahead = max(appt.token_number - now_token, 0)

    est_minutes = people_ahead * (doctor.avg_minutes_per_patient or 10)

    return render(request, "track_token.html", {
        "appt": appt,
        "doctor": doctor,
        "now_token": now_token,
        "people_ahead": people_ahead,
        "est_minutes": est_minutes
    })
