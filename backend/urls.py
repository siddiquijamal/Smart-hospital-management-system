"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.home,name="home"),
    path("loginpage/",views.loginpage,name="loginpage"),
    path("signinpage/",views.signinpage,name="signuppage"),
    path('patient/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('reception/', views.reception_dashboard, name='reception_dashboard'),
    path('logout/',views.logout_view,name="logout"),
    path('appointment/',views.appointment,name = "appointment"),
    path("",include('Patients.urls')),
    path("",include('query.urls')),
    path('', include('appointments.urls')),
    path('', include('Doctors.urls')),
     path("doctor/appointments/", views.doctor_appointments, name="doctor_appointments"),
    path("doctor/appointments/<int:appointment_id>/update/", views.update_appointment_status, name="update_appointment_status"),
    path('bloodbank/',views.blood_bank,name='blood_bank'),
    path('buy_blood/<str:blood_group>/',views.buy_blood,name="buy_blood"),
    

]

