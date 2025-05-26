from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
import uuid

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    unit = models.ForeignKey('MobileUnit', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"

class MobileUnit(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[("active", "Active"), ("inactive", "Inactive")])
    last_check = models.DateTimeField(auto_now=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name

    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("La date de fin doit être postérieure à la date de début.")

    def save(self, *args, **kwargs):
        self.clean()
        # Check if this is an update and status is changing to active
        if self.pk:  # If this is an update
            old_instance = MobileUnit.objects.get(pk=self.pk)
            if old_instance.status != self.status and self.status == "active":
                # Notify assigned staff
                self.notify_assigned_staff()
        super().save(*args, **kwargs)

    def notify_assigned_staff(self):
        # Get all medical and support staff assigned to this unit
        medical_staff = MedicalStaff.objects.filter(assigned_unit=self)
        support_staff = SupportStaff.objects.filter(assigned_unit=self)
        
        # Create message with lifecycle information
        message = f"Votre unité mobile '{self.name}' est maintenant active à {self.location}."
        if self.end_date:
            message += f" La mission se termine le {self.end_date.strftime('%d/%m/%Y')}."
        
        # Create notifications and send emails
        for staff in list(medical_staff) + list(support_staff):
            try:
                user = User.objects.get(email=staff.email)
                # Create notification
                Notification.objects.create(
                    user=user,
                    message=message,
                    unit=self
                )
                
                # Send email
                send_mail(
                    'Unité Mobile Active',
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [staff.email],
                    fail_silently=True,
                )
                
                # If phone number exists, you could send SMS here
                if staff.phone_number:
                    # Placeholder for SMS sending
                    pass
                    
            except User.DoesNotExist:
                continue

    @property
    def is_active(self):
        """Check if the unit is currently active based on dates"""
        now = timezone.now().date()
        if self.end_date and now > self.end_date:
            return False
        return self.status == "active"

    @property
    def days_remaining(self):
        """Calculate days remaining until end date"""
        if not self.end_date:
            return None
        now = timezone.now().date()
        if now > self.end_date:
            return 0
        return (self.end_date - now).days

class MedicalStaff(models.Model):
    ROLE_CHOICES = [
        ('doctor', 'Médecin'),
        ('nurse', 'Infirmier(ère)'),
        ('paramedic', 'Ambulancier(ère)'),
        ('specialist', 'Spécialiste'),
        ('intern', 'Interne'),
        ('other', 'Autre')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    assigned_unit = models.ForeignKey(MobileUnit, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.get_role_display()}"

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit = models.ForeignKey(MobileUnit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.quantity} units)"

class Intervention(models.Model):
    unit = models.ForeignKey(MobileUnit, on_delete=models.CASCADE)
    date = models.DateField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    patients_treated = models.IntegerField()

class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ])
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    medical_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class SupportStaff(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    assigned_unit = models.ForeignKey(MobileUnit, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.role}"

class Unit(models.Model):
    # Existing fields
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance')
    ])
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    last_check = models.DateTimeField(auto_now=True)

    # New fields for real-time tracking
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_location_update = models.DateTimeField(null=True, blank=True)
    is_online = models.BooleanField(default=False)
    battery_level = models.IntegerField(null=True, blank=True)
    signal_strength = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def days_remaining(self):
        if self.end_date:
            return (self.end_date - timezone.now().date()).days
        return None

    @property
    def duration(self):
        if self.end_date:
            return (self.end_date - self.start_date).days
        return None

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    unit = models.ForeignKey(MobileUnit, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.TextField()
    treatment = models.TextField()
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Record for {self.patient} on {self.date}"

class UnitLocation(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    heading = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    battery_level = models.IntegerField(null=True, blank=True)
    signal_strength = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Location update for {self.unit} at {self.timestamp}"
