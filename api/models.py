from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=50)
    diagnostics = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    specialization = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class DoctorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.DOCTOR)


class PatientManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.PATIENT)


class User(AbstractUser):
    class Role(models.TextChoices):
        PATIENT = 'patient', 'Patient'
        DOCTOR = 'doctor', 'Doctor'

    role = models.CharField(max_length=10,
                            choices=Role.choices
                            )
    password = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    objects = UserManager()
    doctors = DoctorManager()
    patients = PatientManager()


class PatientReport(models.Model):
    record_id = models.BigAutoField(primary_key=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    diagnostics = models.TextField()
    observations = models.TextField()
    treatments = models.TextField()

    def __str__(self):
        return f'{self.patient.username}\'s report'
