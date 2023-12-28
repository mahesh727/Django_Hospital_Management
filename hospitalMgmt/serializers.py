# serializers.py
from rest_framework import serializers
from .models import Hospital, Department, Disease, Doctor, Patient, PatientStatusUpdate

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Doctor
        fields = '__all__'

    def create(self, validated_data):
        # Extract the nested department data and create or get the department instance
        department_data = validated_data.pop('department')
        department_instance, created = Department.objects.get_or_create(**department_data)

        # Use the department instance to create the doctor
        doctor_instance = Doctor.objects.create(department=department_instance, **validated_data)
        return doctor_instance

class PatientSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer()
    disease = DiseaseSerializer()
    doctor = DoctorSerializer()

    class Meta:
        model = Patient
        fields = '__all__'

    def create(self, validated_data):
        # Extract the nested hospital, disease, and doctor data and create or get the instances
        hospital_data = validated_data.pop('hospital')
        hospital_instance, created = Hospital.objects.get_or_create(**hospital_data)

        disease_data = validated_data.pop('disease')
        disease_instance, created = Disease.objects.get_or_create(**disease_data)

        doctor_data = validated_data.pop('doctor')
        doctor_instance = DoctorSerializer().create(doctor_data)

        # Use the instances to create the patient
        patient_instance = Patient.objects.create(hospital=hospital_instance, disease=disease_instance, doctor=doctor_instance, **validated_data)
        return patient_instance

class PatientStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientStatusUpdate
        fields = '__all__'

