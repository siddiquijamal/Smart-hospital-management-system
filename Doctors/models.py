from django.db import models

# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField(help_text="Years of experience")
    is_active = models.BooleanField(default=True)
    current_token = models.PositiveIntegerField(default=0)  # 0 means none started
    avg_minutes_per_patient = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"

