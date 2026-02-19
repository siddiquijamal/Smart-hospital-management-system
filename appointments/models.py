from django.db import models
from django.utils import timezone
from Patients.models import Patients
from Doctors.models import Doctor

class Appointment(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending','Pending'),
            ('approved','Approved'),
            ('rejected','Rejected'),
            ('done','Done')
        ],
        default='pending'
    )

    token_number = models.PositiveIntegerField(null=True, blank=True)
    checked_in = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    rejection_reason = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('doctor', 'date', 'token_number') 
        ordering = ['date', 'token_number']

    def __str__(self):
        return f"{self.patient.fullname} → {self.doctor.name} (Token {self.token_number})"
