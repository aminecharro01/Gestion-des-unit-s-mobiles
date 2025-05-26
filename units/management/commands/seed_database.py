from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from units.models import MobileUnit, MedicalStaff, SupportStaff, Equipment, Intervention, Patient, MedicalRecord, Unit
from django.utils import timezone
from datetime import timedelta
import random
import uuid

class Command(BaseCommand):
    help = 'Seeds the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Create admin user if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write('Created admin user')

        # Create mobile units
        units = []
        unit_names = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon']
        locations = ['Paris', 'Lyon', 'Marseille', 'Bordeaux', 'Lille']
        
        for i in range(5):
            unit = MobileUnit.objects.create(
                name=f'Unité Mobile {unit_names[i]}',
                location=locations[i],
                status='active',
                start_date=timezone.now().date() - timedelta(days=random.randint(1, 30)),
                end_date=timezone.now().date() + timedelta(days=random.randint(10, 60))
            )
            units.append(unit)
            self.stdout.write(f'Created mobile unit: {unit.name}')

        # Create medical staff
        medical_staff = []
        medical_staff_names = [
            ('Jean', 'Martin'), ('Marie', 'Dubois'), ('Pierre', 'Bernard'),
            ('Sophie', 'Petit'), ('Luc', 'Robert')
        ]
        
        for first_name, last_name in medical_staff_names:
            username = f'{first_name.lower()}.{last_name.lower()}'
            email = f'{first_name.lower()}.{last_name.lower()}@example.com'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            staff, staff_created = MedicalStaff.objects.get_or_create(
                user=user,
                defaults={
                    'name': f"{first_name} {last_name}",
                    'role': random.choice(['doctor', 'nurse', 'paramedic', 'specialist', 'intern', 'other']),
                    'email': user.email,
                    'phone_number': f'06{random.randint(10000000, 99999999)}',
                    'assigned_unit': random.choice(units)
                }
            )
            if staff_created:
                medical_staff.append(staff)
                self.stdout.write(f'Created medical staff: Dr. {first_name} {last_name}')

        # Create support staff
        support_staff = []
        support_staff_names = [
            ('Thomas', 'Leroy'), ('Julie', 'Moreau'), ('Antoine', 'Girard'),
            ('Camille', 'Roux'), ('Nicolas', 'Fournier')
        ]
        
        for first_name, last_name in support_staff_names:
            username = f'{first_name.lower()}.{last_name.lower()}'
            email = f'{first_name.lower()}.{last_name.lower()}@example.com'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            staff, staff_created = SupportStaff.objects.get_or_create(
                email=user.email,
                defaults={
                    'name': f"{first_name} {last_name}",
                    'role': random.choice(['Logisticien', 'Technicien', 'Administratif']),
                    'phone_number': f'06{random.randint(10000000, 99999999)}',
                    'assigned_unit': random.choice(units)
                }
            )
            if staff_created:
                support_staff.append(staff)
                self.stdout.write(f'Created support staff: {first_name} {last_name}')

        # Create equipment
        equipment_types = ['Ambulance', 'Matériel Médical', 'Générateur', 'Tente Médicale']
        for unit in units:
            for _ in range(random.randint(3, 6)):
                equipment = Equipment.objects.create(
                    name=f'{random.choice(equipment_types)} {unit.name}',
                    unit=unit,
                    quantity=random.randint(1, 5)
                )
                self.stdout.write(f'Created equipment: {equipment.name}')

        # Create patients
        patients = []
        patient_names = [
            ('Emma', 'Lefebvre'), ('Lucas', 'Garcia'), ('Léa', 'David'),
            ('Hugo', 'Bertrand'), ('Chloé', 'Morel'), ('Jules', 'Laurent'),
            ('Manon', 'Simon'), ('Arthur', 'Michel'), ('Inès', 'Leroy'),
            ('Louis', 'Roux')
        ]
        
        for first_name, last_name in patient_names:
            patient = Patient.objects.create(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=timezone.now() - timedelta(days=random.randint(365*18, 365*80)),
                gender=random.choice(['M', 'F']),
                phone_number=f'06{random.randint(10000000, 99999999)}',
                address=f'{random.randint(1, 100)} rue {random.choice(["de la Paix", "Victor Hugo", "République", "Liberté"])}, {random.choice(["Paris", "Lyon", "Marseille", "Bordeaux", "Lille"])}'
            )
            patients.append(patient)
            self.stdout.write(f'Created patient: {first_name} {last_name}')

        # Create interventions
        intervention_types = ['Urgence', 'Consultation', 'Suivi', 'Vaccination']
        for patient in patients:
            for _ in range(random.randint(1, 3)):
                intervention = Intervention.objects.create(
                    unit=random.choice(units),
                    date=timezone.now() - timedelta(days=random.randint(1, 30)),
                    location=random.choice(locations),
                    description=f'Intervention de type {random.choice(intervention_types)} pour {patient.first_name} {patient.last_name}',
                    patients_treated=random.randint(1, 5)
                )
                self.stdout.write(f'Created intervention for {patient.first_name} {patient.last_name}')

        # Create medical records
        diagnoses = ['Grippe', 'Fracture', 'Hypertension', 'Diabète', 'Asthme']
        treatments = ['Antibiotiques', 'Antalgiques', 'Insuline', 'Ventoline', 'Paracétamol']
        
        for patient in patients:
            for _ in range(random.randint(1, 2)):
                record = MedicalRecord.objects.create(
                    patient=patient,
                    unit=random.choice(units),
                    diagnosis=random.choice(diagnoses),
                    treatment=random.choice(treatments),
                    notes=f'Notes médicales pour {patient.first_name} {patient.last_name}',
                    date=timezone.now() - timedelta(days=random.randint(1, 30))
                )
                self.stdout.write(f'Created medical record for {patient.first_name} {patient.last_name}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded database')) 