# doctorapp/urls.py
from django.urls import path
from .views import (
    DoctorListCreateView, DoctorDetailView,
    PatientListCreateView, PatientDetailView,
    AvailabilityListCreateView, AvailabilityDetailView,
    AppointmentListCreateView, AppointmentDetailView
)

urlpatterns = [
    path('doctors/', DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('patients/', PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('availabilities/', AvailabilityListCreateView.as_view(), name='availability-list-create'),
    path('availabilities/<int:pk>/', AvailabilityDetailView.as_view(), name='availability-detail'),
    path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
]
