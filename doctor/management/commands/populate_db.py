# doctorapp/management/commands/populate_db.py
import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import CustomUser
from doctor.models import Doctor, Patient, Availability, Appointment

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def handle(self, *args, **kwargs):
        # Create doctors
        for _ in range(10):
            user = CustomUser.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123',
                role='doctor'
            )
            doctor = Doctor.objects.create(
                user=user,
                name=fake.name(),
                specialization=fake.job(),
                email=user.email,
                phone_number=fake.phone_number(),
                profile_picture=None
            )
            # Create availability for each doctor
            for _ in range(5):
                day_of_week = fake.random_element(elements=('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'))
                start_time = fake.time_object(end_datetime=None)
                end_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=2)).time()
                Availability.objects.create(
                    doctor=doctor,
                    day_of_week=day_of_week,
                    start_time=start_time,
                    end_time=end_time
                )

        # Create patients
        for _ in range(10):
            user = CustomUser.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123',
                role='patient'
            )
            patient = Patient.objects.create(
                user=user,
                name=fake.name(),
                email=user.email,
                phone_number=fake.phone_number()
            )

        # Create appointments
        doctors = Doctor.objects.all()
        patients = Patient.objects.all()
        for _ in range(20):
            doctor = random.choice(doctors)
            patient = random.choice(patients)
            appointment_date = fake.date_between(start_date='today', end_date='+30d')
            start_time = random.choice(Availability.objects.filter(doctor=doctor).values_list('start_time', flat=True))
            Appointment.objects.create(
                doctor=doctor,
                patient=patient,
                appointment_date=appointment_date,
                appointment_time=start_time
            )

        self.stdout.write(self.style.SUCCESS('Database populated with fake data'))
