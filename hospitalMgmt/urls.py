from django.urls import path
from .views import PatientStatusView, AllHospitalVisitsView, PatientCreateView, StatusUpdateView,Login,GetHospital,GetDcotor,GetDepartment,GetDisease,DepartmentView,HospitalView,DepartmentCreateView,AddDepartment,DepartmentByHospitalView,DoctorView,DiseaseView,PatientRecordCreate

'''urlpatterns = [
    path('patient-status/<str:name>/', PatientStatusView.as_view(), name='patient-status'),
    path('all-hospital-visits/<int:patient_id>/', AllHospitalVisitsView.as_view(), name='all-hospital-visits'),
    path('create-patient/', PatientCreateView.as_view(), name='create-patient'),
    path('status-update/', StatusUpdateView.as_view(), name='status-update')

    path('login/', Login.as_view(), name='login'),

    path('get-hospital/',GetHospital.as_view(),name='get-hospital'),
    path('get-doctor/<int:hospital_id>/',GetDcotor.as_view(),name='get-doctor'),
    path('get-disease/',GetDisease.as_view(),name='get-disease'),

    path('hospitals/', HospitalListCreateView.as_view(), name='hospital-list-create'),
    path('hospitals/<int:hospital_id>/departments/', DepartmentCreateView.as_view(), name='department-create'),
]'''

urlpatterns = [
    
    path('create-patient/', PatientCreateView.as_view(), name='create-patient'),
    path('create-hospital/', HospitalView.as_view(), name='hospital-create'),
    path('create-department/', DepartmentCreateView.as_view(), name='department-create'),
    path('add-department/',AddDepartment.as_view(),name='create-department'),
    path('create-doctor/',DoctorView.as_view(),name='create-doctor'),
    path('create-disease/',DiseaseView.as_view(),name='create-disease'),
    path('create-record/',PatientRecordCreate.as_view(),name='create-record'),
    path('get-department/',GetDepartment.as_view(),name='get-department'),
    path('get-hospital/',GetHospital.as_view(),name='get-hospital'),
    path('get-department/<int:hospital>/', DepartmentByHospitalView.as_view(), name='get-departments-by-hospital'),
    path('all-hospital-visits/<int:patient_id>/', AllHospitalVisitsView.as_view(), name='all-hospital-visits'),
    path('patient-status/<str:name>/', PatientStatusView.as_view(), name='patient-status'),

    
    

    path('login/', Login.as_view(), name='login'),

   
]

