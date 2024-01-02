from django.contrib import admin
from .models import Hospital, Department, Disease, Doctor, Patient, PatientStatusUpdate

admin.site.register(Hospital)
admin.site.register(Department)
admin.site.register(Disease)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(PatientStatusUpdate)
