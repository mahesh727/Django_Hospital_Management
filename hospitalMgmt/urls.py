from django.urls import path
from .views import PatientStatusView, AllHospitalVisitsView, PatientCreateView, StatusUpdateView,Login,GetHospital,GetDcotor,GetDisease

urlpatterns = [
    path('patient-status/<str:name>/', PatientStatusView.as_view(), name='patient-status'),
    path('all-hospital-visits/<int:patient_id>/', AllHospitalVisitsView.as_view(), name='all-hospital-visits'),
    path('create-patient/', PatientCreateView.as_view(), name='create-patient'),
    path('status-update/', StatusUpdateView.as_view(), name='status-update'),

    path('login/', Login.as_view(), name='login'),

    path('get-hospital/',GetHospital.as_view(),name='get-hospital'),
    path('get-doctor/<int:hospital_id>/',GetDcotor.as_view(),name='get-doctor'),
    path('get-disease/',GetDisease.as_view(),name='get-disease'),
]
