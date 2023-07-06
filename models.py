from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Hospital(models.Model):
    name = models.CharField(max_length=100)
    class TypeChoices(models.TextChoices):
        PRIVATE = "private", "Private"
        PUBLIC = "public", "Public"
        
    type = models.CharField(max_length=20, choices=TypeChoices.choices)
    
    def __str__(self) -> str:
        return self.name

class HospitalSection(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="sections", null=True)
    name = models.CharField(max_length=100)
    appwrite_id = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name
    
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="doctor_profile")
    section = models.ForeignKey(HospitalSection, on_delete=models.CASCADE, related_name="doctors")
    doctor_name = models.CharField(max_length=100)
    doctor_description = models.CharField(max_length=100, null=True, blank=True)
    doctor_address = models.CharField(max_length=100, null=True, blank=True)
    waiting_time = models.IntegerField(null=True, blank=True)
    doctor_price = models.FloatField(null=True, blank=True)
    from_time = models.CharField(max_length=100)
    to_time = models.CharField(max_length=100)
    Work_day = models.CharField(max_length=100, null=True, blank=True)
    appwrite_id = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    session_price = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return self.doctor_name
    
class Patient(User):
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    
    
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"


class Reservation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="reservations")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="reservations")
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.doctor} - {self.patient} - {self.date}"
    

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="consultations")
    section = models.ForeignKey(HospitalSection, on_delete=models.CASCADE, related_name="consultations")
    type = models.CharField(max_length=20)
    age = models.IntegerField()
    weight = models.FloatField()
    has_any_disease = models.BooleanField(default=False)
    description = models.TextField()    
    image = models.ImageField(upload_to="consultation_images", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reply = models.TextField(null=True, blank=True)
    doctor_replied = models.ForeignKey(Doctor, on_delete=models.SET_NULL, related_name="consultations_replied", null=True, blank=True)