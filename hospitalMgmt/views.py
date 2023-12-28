# views.py
from rest_framework import generics
from .models import Hospital, Department, Disease, Doctor, Patient, PatientStatusUpdate
from rest_framework.response import Response
from rest_framework import status
from .models import Hospital, Department, Disease, Doctor, Patient, PatientStatusUpdate
from .serializers import (
    HospitalSerializer,
    DepartmentSerializer,
    DiseaseSerializer,
    DoctorSerializer,
    PatientSerializer,
    PatientStatusUpdateSerializer,
)

class HospitalView(generics.CreateAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

class DepartmentView(generics.CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DiseaseView(generics.CreateAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer

class DoctorView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class PatientView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientStatusUpdateView(generics.CreateAPIView):
    queryset = PatientStatusUpdate.objects.all()
    serializer_class = PatientStatusUpdateSerializer


class PatientStatusView(generics.RetrieveAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    lookup_field = 'name'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        latest_status_update = PatientStatusUpdate.objects.filter(patient=instance).order_by('-timestamp').first()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['latest_status_update'] = PatientStatusUpdateSerializer(latest_status_update).data if latest_status_update else None
        return Response(data)

class AllHospitalVisitsView(generics.ListAPIView):
    queryset = PatientStatusUpdate.objects.filter(update_type__in=['Admitted', 'Discharged'])
    serializer_class = PatientStatusUpdateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.order_by('timestamp')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PatientCreateView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(status='Admitted')
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class StatusUpdateView(generics.CreateAPIView):
    queryset = PatientStatusUpdate.objects.all()
    serializer_class = PatientStatusUpdateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.validated_data['patient']
        update_type = serializer.validated_data['update_type']
        if update_type in ['Admitted', 'Discharged']:
            patient.status = update_type
            patient.save()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

