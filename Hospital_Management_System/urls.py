"""
URL configuration for Hospital_Management_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
'''from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]'''
'''
from django.urls import path
from hospitalMgmt.views import HospitalView, DepartmentView, DiseaseView, DoctorView, PatientView, PatientStatusUpdateView

urlpatterns = [
    path('create-hospital/', HospitalView.as_view(), name='create-hospital'),
    path('create-department/', DepartmentView.as_view(), name='create-department'),
    path('create-disease/', DiseaseView.as_view(), name='create-disease'),
    path('create-doctor/', DoctorView.as_view(), name='create-doctor'),
    path('create-patient/', PatientView.as_view(), name='create-patient'),
    path('status-update/', PatientStatusUpdateView.as_view(), name='status-update'),
]'''
from django.contrib import admin
from django.urls import path, include
#from hospitalMgmt.views import HospitalView, DepartmentView, DiseaseView, DoctorView, PatientView, PatientStatusUpdateView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('hospitalMgmt.urls'))# Include the URLs from your app
]

'''path('admin/create-hospital/', HospitalView.as_view(), name='create-hospital'),
    path('admin/create-department/', DepartmentView.as_view(), name='create-department'),
    path('admin/create-disease/', DiseaseView.as_view(), name='create-disease'),
    path('admin/create-doctor/', DoctorView.as_view(), name='create-doctor'),
    path('admin/create-patient/', PatientView.as_view(), name='create-patient'),
    path('admin/status-update/', PatientStatusUpdateView.as_view(), name='status-update'),'''

