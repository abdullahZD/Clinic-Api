from rest_framework import serializers
from .models import Doctor, Patient, Availability, Appointment
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):
        doctor = data['doctor']
        appointment_date = data['appointment_date']
        appointment_time = data['appointment_time']

        # Check if the appointment time is within the available times for the doctor
        day_of_week = appointment_date.strftime('%A')
        try:
            availability = Availability.objects.get(doctor=doctor, day_of_week=day_of_week)
            if not (availability.start_time <= appointment_time < availability.end_time):
                raise ValidationError('The appointment time is not within the available times for this doctor.')
        except Availability.DoesNotExist:
            raise ValidationError('The doctor does not have available times set for this day.')

        # Ensure each appointment is 20 minutes long
        start_time = datetime.combine(appointment_date, appointment_time)
        end_time = start_time + timedelta(minutes=20)

        # Check if the appointment overlaps with another appointment for the same doctor
        overlapping_appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time__lt=end_time.time(),
            appointment_time__gte=appointment_time
        ).exclude(pk=self.instance.pk if self.instance else None)

        if overlapping_appointments.exists():
            raise ValidationError('This appointment time is already taken.')

        return data
