from rest_framework import generics
from .models import Hospital, Department, Disease, Doctor, Patient, PatientStatusUpdate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import (
    HospitalSerializer,
    DepartmentSerializer,
    DiseaseSerializer,
    DoctorSerializer,
    PatientSerializer,
    PatientStatusUpdateSerializer,
)
from django.contrib.auth import authenticate

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
class Login(APIView):
   def post(self, request, *args, **kwargs):
       
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        print(username)
        print(password)
        
        user = authenticate(username=username, password=password)

        if user is not None:

           
            return Response({'message': 'Credentials are correct'}, status=status.HTTP_200_OK)
        else:
            
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            

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
        print(request.method)
        patient_id=request.data.get('patient'),
            
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


class GetHospital(APIView):
    def get(self, request, format=None):
        hospitals = Hospital.objects.all()
        serializer = HospitalSerializer(hospitals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class GetDcotor(APIView):
    def get(self, request, hospital_id):
        try:
            doctors = Doctor.objects.filter(hospital__id=hospital_id)
            serializer = DoctorSerializer(doctors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class GetDisease(APIView):
    def get(self, request, format=None):
        hospitals = Disease.objects.all()
        serializer = DiseaseSerializer(hospitals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)