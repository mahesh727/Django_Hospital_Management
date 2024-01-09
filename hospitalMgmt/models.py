from django.db import models

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

class Department(models.Model):
    name = models.CharField(max_length=255)

class Disease(models.Model):
    name = models.CharField(max_length=255)

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
        hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

class Patient(models.Model):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=10)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

class PatientStatusUpdate(models.Model):
    STATUS_CHOICES = [
        ('Primary_Check','Primary_Check'),
        ('Consultation','Consultation'),
        ('Admitted','Admitted'),
        ('Under_treatment','Under_treatment'),
        ('Discharged','Discharged')
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    update_type = models.CharField(max_length=20, choices=STATUS_CHOICES)
    remarks = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
