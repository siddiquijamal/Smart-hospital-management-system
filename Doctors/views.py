from django.shortcuts import render
from Doctors.models import Doctor
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from appointments.models import Appointment
from django.db.models import Max

def doctors_detail(request):
    doctors = Doctor.objects.all().order_by("name")
    return render(request, "doctors_detail.html", {"doctors": doctors})






def doctor_queue(request):
    if request.session.get("role","").lower() != "doctor":
        return redirect("loginpage")

    doctor_id = request.session.get("doctor_id")
    doctor = get_object_or_404(Doctor, id=doctor_id)

    appointments = Appointment.objects.filter(
        doctor=doctor,
        date=timezone.now().date(),
        status__in=["pending", "approved"]
    ).select_related("patient").order_by("token_number")

    return render(request, "doctor_queue.html", {
        "doctor": doctor,
        "appointments": appointments
    })
    
    
def next_token(request):
    if request.session.get("role","").lower() != "doctor":
        return redirect("loginpage")

    doctor_id = request.session.get("doctor_id")
    doctor = get_object_or_404(Doctor, id=doctor_id)

   
    nxt = Appointment.objects.filter(
        doctor=doctor,
        date=timezone.now().date(),
        status__in=["pending","approved"],
        token_number__gt=doctor.current_token
    ).order_by("token_number").first()

    if not nxt:
        messages.info(request, "No more tokens for today.")
        return redirect("doctor_queue")

    doctor.current_token = nxt.token_number
    doctor.save()

    messages.success(request, f"Now serving token #{doctor.current_token}")
    return redirect("doctor_queue")



def mark_done(request, appointment_id):
    if request.session.get("role","").lower() != "doctor":
        return redirect("loginpage")

    doctor_id = request.session.get("doctor_id")
    doctor = get_object_or_404(Doctor, id=doctor_id)

    appt = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    appt.status = "done"
    appt.save()

    return redirect("doctor_queue")
