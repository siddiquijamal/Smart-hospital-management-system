from .views import book_appointment
from django.urls import path,include
from appointments import views

urlpatterns = [
    path('appointmentspage/', views.book_appointment, name='appointmentspage'),
    path(
        'approve/<int:appointment_id>/',
        views.approve_appointment,
        name='approve_appointment'
    ),
]