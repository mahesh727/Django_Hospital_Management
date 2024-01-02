from rest_framework import generics
from .models import Hospital, Department, Disease, Doctor, Patient, PatientStatusUpdate
from rest_framework.response import Response
from rest_framework import status
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
    #print(queryset)
    serializer_class = PatientSerializer
    lookup_field = 'name'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        latest_status_update = PatientStatusUpdate.objects.filter(patient=instance).order_by('-timestamp').first()

        if latest_status_update:
            status_serializer = PatientStatusUpdateSerializer(latest_status_update)
            return Response({"patient_status": status_serializer.data['update_type']})

        return Response({"patient_status": "No status update available"})

class AllHospitalVisitsView(generics.ListAPIView):
    serializer_class = PatientStatusUpdateSerializer

    def get_queryset(self):
        patient_id = self.kwargs.get('patient_id')  
        return PatientStatusUpdate.objects.filter(patient__id=patient_id)

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
        patient = serializer.save()

        
        PatientStatusUpdate.objects.create(patient=patient, update_type='primary_check')

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class StatusUpdateView(generics.CreateAPIView):
    
    queryset = PatientStatusUpdate.objects.all()
    serializer_class = PatientStatusUpdateSerializer

    def create(self, request, *args, **kwargs):
        # Extract patient ID from the request data
        #patient_id = request.data.get('patient_id')

        # Check if patient_id is provided in the request data
        #if not patient_id:
            #return Response({"patient_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        # Create a dictionary with patient_id and other data for the serializer
        #print(request.method)
        #patient_id=request.data.get('patient'),
        '''try:
            patient=Patient.objects.get(id=patient_id)
        except:
            return Response({'error':'Patient not found'},status=status.HTTP_404_NOT_FOUND)'''
            
        data = {
            'patient':request.data.get('patient'),
            'update_type': request.data.get('update_type'),
            'remarks': request.data.get('remarks'),
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

     

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

'''queryset = PatientStatusUpdate.objects.all()
    serializer_class = PatientStatusUpdateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.validated_data['patient']
        update_type = serializer.validated_data['update_type']
        #if update_type in ['Admitted', 'Discharged']:
        patient.status = update_type
        patient.save()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)'''
'''queryset = PatientStatusUpdate.objects.all()
    serializer_class = PatientStatusUpdateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract patient ID from the request data or other sources
        patient_id = serializer.validated_data['patient'].id

        # You can use patient_id for any further processing or logging

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)'''