# urls.py
from django.urls import path
from .views import PatientStatusView, AllHospitalVisitsView, PatientCreateView, StatusUpdateView

urlpatterns = [
    path('patient-status/<str:name>/', PatientStatusView.as_view(), name='patient-status'),
    path('all-hospital-visits/', AllHospitalVisitsView.as_view(), name='all-hospital-visits'),
    path('create-patient/', PatientCreateView.as_view(), name='create-patient'),
    path('status-update/', StatusUpdateView.as_view(), name='status-update'),
]
