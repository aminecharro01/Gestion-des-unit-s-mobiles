from django.core.management.base import BaseCommand
from units.models import MedicalStaff, MobileUnit
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Sets up initial medical staff and assigns them to units'

    def handle(self, *args, **kwargs):
        # Create mobile units if they don't exist
        unit1, created = MobileUnit.objects.get_or_create(
            name="Unité Mobile 1",
            defaults={
                'location': "Casablanca",
                'status': "active"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created unit: {unit1}'))

        unit2, created = MobileUnit.objects.get_or_create(
            name="Unité Mobile 2",
            defaults={
                'location': "Rabat",
                'status': "active"
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created unit: {unit2}'))

        # Create medical staff
        medical_staff_data = [
            {
                'name': "Dr. Ahmed Benali",
                'role': "Médecin",
                'email': "ahmed.benali@example.com",
                'phone_number': "0612345678",
                'assigned_unit': unit1,
                'username': 'ahmed.benali',
                'password': 'password123'
            },
            {
                'name': "Dr. Fatima Zahra",
                'role': "Médecin",
                'email': "fatima.zahra@example.com",
                'phone_number': "0623456789",
                'assigned_unit': unit1,
                'username': 'fatima.zahra',
                'password': 'password123'
            },
            {
                'name': "Dr. Karim Hassan",
                'role': "Médecin",
                'email': "karim.hassan@example.com",
                'phone_number': "0634567890",
                'assigned_unit': unit2,
                'username': 'karim.hassan',
                'password': 'password123'
            },
            {
                'name': "Dr. Leila Mansouri",
                'role': "Médecin",
                'email': "leila.mansouri@example.com",
                'phone_number': "0645678901",
                'assigned_unit': unit2,
                'username': 'leila.mansouri',
                'password': 'password123'
            }
        ]

        for staff_data in medical_staff_data:
            # Create or get user
            username = staff_data.pop('username')
            password = staff_data.pop('password')
            
            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': staff_data['email'],
                    'first_name': staff_data['name'].split()[1],
                    'last_name': staff_data['name'].split()[2],
                    'is_staff': True
                }
            )
            
            if user_created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))

            # Create or update medical staff
            staff, staff_created = MedicalStaff.objects.get_or_create(
                email=staff_data['email'],
                defaults={
                    **staff_data,
                    'user': user
                }
            )
            
            if staff_created:
                self.stdout.write(self.style.SUCCESS(f'Created medical staff: {staff}'))
            else:
                # Update existing staff's unit assignment and user
                staff.assigned_unit = staff_data['assigned_unit']
                staff.user = user
                staff.save()
                self.stdout.write(self.style.SUCCESS(f'Updated medical staff: {staff}')) 