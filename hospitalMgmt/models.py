'''from django.db import models
from phonenumber_field.modelfields import PhoneNumberField'''

'''class Hospital(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

class Department(models.Model):
    name = models.CharField(max_length=255)'''

'''class Hospital(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    departments = models.ManyToManyField('Department', related_name='hospital')

class Department(models.Model):
    name = models.CharField(max_length=255)
    hospitals = models.ManyToManyField('Hospital', related_name='department')

class Disease(models.Model):
    name = models.CharField(max_length=255)
    symptoms= models.TextField(default='')

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    contact_number = PhoneNumberField(null=False, blank=True, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

class Patient(models.Model):
    name = models.CharField(max_length=255)
    contact_number = PhoneNumberField(null=False, blank=True, unique=True)
    date_of_birth = models.DateField(default=None)



class PatientRecord(models.Model):
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
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)'''
from django.db import models
from django.core.validators import RegexValidator
#from phonenumber_field.modelfields import PhoneNumberField

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

class Department(models.Model):
    name = models.CharField(max_length=255)
    hospitals = models.ManyToManyField('Hospital', related_name='department')

class Disease(models.Model):
    name = models.CharField(max_length=255)
    symptoms = models.TextField(default='')

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=10,  blank=True,  null=True,  validators=[RegexValidator(regex=r'^\d{10}$')])
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, default=1)

class Patient(models.Model):
    GENDER_CHOICES=[
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others')
    ]
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=10,  blank=True,  null=True,  validators=[RegexValidator(regex=r'^\d{10}$')])
    date_of_birth = models.DateField(default=None)
    gender=models.CharField(choices=GENDER_CHOICES,max_length=6)

class PatientRecord(models.Model):
    STATUS_CHOICES = [
        ('Primary_Check', 'Primary_Check'),
        ('Consultation', 'Consultation'),
        ('Admitted', 'Admitted'),
        ('Under_treatment', 'Under_treatment'),
        ('Discharged', 'Discharged')
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    update_type = models.CharField(max_length=15, choices=STATUS_CHOICES)
    remarks = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=1)

