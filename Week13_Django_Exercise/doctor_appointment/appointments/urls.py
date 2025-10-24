from django.urls import path
from appointments import views

urlpatterns = [
    path('doctors/', views.DoctorList.as_view(), name='doctor-list'),
    path('patients/', views.PatientList.as_view(), name='patient-list'),
    path('appointments/', views.AppointmentList.as_view(), name='appointments-list'),
    path('appointments/<int:pk>/', views.AppointmentDetail.as_view(), name='appointments-detail'),
]