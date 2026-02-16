
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("doctors/", views.doctors_detail, name="doctor_detail"),
    path("doctor/queue/", views.doctor_queue, name="doctor_queue"),
    path("doctor/next/", views.next_token, name="next_token"),
    path("doctor/done/<int:appointment_id>/", views.mark_done, name="mark_done"),
]