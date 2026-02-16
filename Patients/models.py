from django.db import models

# Create your models here.


class Patients(models.Model):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('receptionist', 'Receptionist'),
    ]
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.fullname} ({self.role})"

    