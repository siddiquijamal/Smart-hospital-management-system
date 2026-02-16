
from django.urls import path,include

from Patients import views

urlpatterns = [
    path('signindetails/',views.signindetail,name = "signindetail"),
    path('logindetail/',views.logindetail,name = "logindetail"),
    path("my_appointments/", views.patient_appointments_page, name="my_appointments"),
    path("appointments/track/<int:appointment_id>/", views.track_token, name="track_token"),
]
