
from django.db import transaction
from django.db.models import Max
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404, redirect
from .models import Appointment
from Patients.models import Patients
from Doctors.models import Doctor

# Create your views here.


@transaction.atomic
def book_appointment(request):
    if 'user_id' not in request.session:
        return redirect('loginpage')

    doctors = Doctor.objects.all()

    if request.method == "POST":
        date_str = request.POST.get('date')
        time = request.POST.get('time')
        doctor_id = request.POST.get('doctor_id')

        date = parse_date(date_str)
        if not date:
            return render(request, 'book_appointment.html', {'doctors': doctors, 'error': 'Invalid date'})

        patient = Patients.objects.get(id=request.session['user_id'])
        doctor = Doctor.objects.get(id=doctor_id)

        if Appointment.objects.filter(patient=patient, doctor=doctor, date=date, time=time).exists():
            return render(request, 'book_appointment.html', {'doctors': doctors, 'error': 'You already booked this slot.'})

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=date,
            time=time,
            token_number=None,     
            status="pending"
        )

        return redirect('my_appointments')

    return render(request, 'book_appointment.html', {'doctors': doctors})



@transaction.atomic
def approve_appointment(request, appointment_id):
    appt = get_object_or_404(Appointment.objects.select_for_update(), id=appointment_id)

    appt.status = "approved"

    if appt.token_number is None:
        last_token = (
            Appointment.objects
            .select_for_update()
            .filter(
                doctor=appt.doctor,
                date=appt.date,
                status__in=["approved", "done"],
                token_number__isnull=False
            )
            .aggregate(mx=Max("token_number"))["mx"] or 0
        )
        appt.token_number = last_token + 1

    appt.save()
    return redirect("doctor_dashboard")