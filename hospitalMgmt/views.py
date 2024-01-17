from rest_framework import generics
from .models import Hospital, Department, Disease, Doctor, Patient, PatientRecord
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from .serializers import (
    HospitalSerializer,
    DepartmentSerializer,
    DiseaseSerializer,
    DoctorSerializer,
    PatientSerializer,
    PatientRecordSerializer,
)
from django.contrib.auth import authenticate
import logging

logger = logging.getLogger(__name__)

class HospitalView(generics.CreateAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer


'''class DepartmentCreateView(generics.CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def perform_create(self, serializer):
        hospital_id = self.kwargs.get('hospital_id')
        hospital = Hospital.objects.get(pk=hospital_id)
        serializer.save(hospital=hospital)'''


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
    queryset = PatientRecord.objects.all()
    serializer_class = PatientRecordSerializer


class PatientStatusView(generics.RetrieveAPIView):
    queryset = Patient.objects.all()
    #print(queryset)
    serializer_class = PatientSerializer
    lookup_field = 'name'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        latest_status_update = PatientRecord.objects.filter(patient=instance).order_by('-timestamp').first()
        print(latest_status_update)
        if latest_status_update:
            status_serializer = PatientRecordSerializer(latest_status_update)
            #print(status_serializer.data['update_type'])
            return Response({"patient_status": status_serializer.data['update_type']})
        return Response({"patient_status": "No status update available"})           

class AllHospitalVisitsView(generics.ListAPIView):
    serializer_class = PatientRecordSerializer

    def get_queryset(self):
        patient_id = self.kwargs.get('patient_id')  
        return PatientRecord.objects.filter(patient__id=patient_id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.order_by('timestamp')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PatientCreateView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def create(self, request, *args, **kwargs):
        print(request.data.get('name'))
        print(request.data.get('gender'))
        print(request.data.get('contact_number'))
        print(request.data.get('date_of_birth'))
        serializer = self.get_serializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            patient = serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        #PatientRecord.objects.create(patient=patient, update_type='primary_check')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddDepartment(generics.CreateAPIView):
    serializer_class = DepartmentSerializer

    def create(self, request, *args, **kwargs):
        hospital_data = request.data.get('hospital')
        department_list = request.data.get('department',[])

        print(department_list)
        hospital_instance = Hospital.objects.get(id=hospital_data)
        

        for department_data in department_list:
        
            try:
                department_instance = Department.objects.get(id=department_data)

                
                if department_instance in hospital_instance.department.all():#hospital_instance.departments.all():
                    return Response({'error': f'Department {department_instance.id} is already associated with the hospital.'},
                                    status=status.HTTP_400_BAD_REQUEST)

                hospital_instance.department.add(department_instance)
            except Department.DoesNotExist:
                return Response({'error': 'One or more departments not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Associations created successfully.'}, status=status.HTTP_201_CREATED)


class DepartmentCreateView(generics.CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        
        
        if Department.objects.filter(name=name).exists():
            error_message = f"Department with name '{name}' already exists."
            response_data = {"error": error_message}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        try :
            department=Department.objects.create(name=request.data.get('name'))
            response_data = {"message": "Department created successfully"}
            return Response(response_data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            error_message = f"Error creating department: {e}"
            response_data = {"error": error_message}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)



        

class StatusUpdateView(generics.CreateAPIView):
    
    queryset = PatientRecord.objects.all()
    serializer_class = PatientRecordSerializer

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



'''class DepartmentByHospitalView(ListAPIView):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        hospital_id = self.request.GET.get('hospital')

        if not hospital_id:
            #depts = Department.objects.filter(hospi)
            return Department.objects.none()

        queryset = Department.objects.filter(hospitals=hospital_id)'''
'''class DepartmentByHospitalView(ListAPIView):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        hospital_id = self.kwargs.get('hospital')
          
        #hospital = Hospital.objects.get(id=hospital)
        hospital_obj=Hospital.objects.get(id=hospital_id)
        
        if not hospital_obj:
            return Department.objects.none()

        queryset = Department.objects.filter(hospitals=hospital_obj)
        print(queryset)
        return queryset'''
class DepartmentByHospitalView(ListAPIView):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        hospital_id = self.kwargs.get('hospital')

        try:
            hospital_obj = Hospital.objects.get(id=hospital_id)
        except Hospital.DoesNotExist:
            logger.error(f"Hospital with ID {hospital_id} does not exist.")
            return Department.objects.none()
        queryset = Department.objects.filter(hospitals=hospital_obj)
        logger.debug(f"Queryset for hospital {hospital_obj}: {queryset}")

        return queryset

class PatientRecordCreate(generics.CreateAPIView):
      queryset=PatientRecord.objects.all()
      serializer_class=PatientRecordSerializer

      def create(self,request,*args,**kwargs):
          serializer = self.get_serializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          self.perform_create(serializer)
          return Response(serializer.data,status=201)
        
    







class Login(APIView):
   def post(self, request, *args, **kwargs):
       
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        #print(username)
        print(username)
        print(password)
        
        user = authenticate(username=username, password=password)
        #print(user)
        if user is not None:
            return Response({'message': 'Credentials are correct'}, status=status.HTTP_200_OK)
        else:
            
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

class GetHospital(APIView):
    def get(self, request, format=None):
        hospitals = Hospital.objects.all()
        serializer = HospitalSerializer(hospitals, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetDepartment(APIView):
    def get(self, request, format=None):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
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











'''
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Hospital, Department, Disease, Doctor, Patient, PatientRecord
from .serializers import (
    HospitalSerializer,
    DepartmentSerializer,
    DiseaseSerializer,
    DoctorSerializer,
    PatientSerializer,
    PatientStatusUpdateSerializer,
)
from django.contrib.auth import authenticate


class HospitalListCreateView(APIView):
    def get(self, request, format=None):
        hospitals = Hospital.objects.all()
        serializer = HospitalSerializer(hospitals, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentCreateView(APIView):
    def post(self, request, hospital_id, format=None):
        hospital = Hospital.objects.get(pk=hospital_id)
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hospital=hospital)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiseaseView(APIView):
    def post(self, request, format=None):
        serializer = DiseaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorView(APIView):
    def post(self, request, format=None):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientView(APIView):
    def post(self, request, format=None):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientCreateView(APIView):
    def get(self, request, *args, **kwargs):
        # Implement your logic for handling GET requests here
        # For example, you can return a list of existing patients
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request,*args,**kwargs):
        serializer=PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PatientStatusUpdateView(APIView):
    def post(self, request, format=None):
        serializer = PatientStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientStatusView(APIView):
    def get(self, request, name, format=None):
        patient = Patient.objects.get(name=name)
        latest_status_update = PatientRecord.objects.filter(patient=patient).order_by('-timestamp').first()
        if latest_status_update:
            status_serializer = PatientStatusUpdateSerializer(latest_status_update)
            return Response({"patient_status": status_serializer.data['update_type']})
        return Response({"patient_status": "No status update available"})


class Login(APIView):
    def post(self, request, format=None):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({'message': 'Credentials are correct'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class AllHospitalVisitsView(APIView):
    def get(self, request, patient_id, format=None):
        visits = PatientRecord.objects.filter(patient__id=patient_id).order_by('timestamp')
        serializer = PatientStatusUpdateSerializer(visits, many=True)
        return Response(serializer.data)


class PatientCreateView(APIView):
    def post(self, request, format=None):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()
            PatientRecord.objects.create(patient=patient, update_type='primary_check')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusUpdateView(APIView):
    def post(self, request, format=None):
        data = {
            'patient': request.data.get('patient'),
            'update_type': request.data.get('update_type'),
            'remarks': request.data.get('remarks'),
        }
        serializer = PatientStatusUpdateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetHospital(APIView):
    def get(self, request, format=None):
        hospitals = Hospital.objects.all()
        serializer = HospitalSerializer(hospitals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetDcotor(APIView):
    def get(self, request, hospital_id, format=None):
        doctors = Doctor.objects.filter(hospital__id=hospital_id)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetDisease(APIView):
    def get(self, request, format=None):
        diseases = Disease.objects.all()
        serializer = DiseaseSerializer(diseases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)'''

