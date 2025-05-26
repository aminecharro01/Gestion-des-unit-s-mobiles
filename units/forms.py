from django import forms
from .models import MobileUnit, MedicalStaff, SupportStaff, Equipment, Intervention, Patient, MedicalRecord, Unit
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MobileUnitForm(forms.ModelForm):
    class Meta:
        model = MobileUnit
        fields = ['name', 'location', 'status', 'start_date', 'end_date']
        labels = {
            'name': 'Nom de l\'unité',
            'location': 'Localisation',
            'status': 'Statut',
            'start_date': 'Date de début',
            'end_date': 'Date de fin'
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MedicalStaffForm(forms.ModelForm):
    class Meta:
        model = MedicalStaff
        fields = ['name', 'role', 'email', 'phone_number', 'assigned_unit', 'user']
        labels = {
            'name': 'Nom complet',
            'role': 'Rôle',
            'email': 'Email',
            'phone_number': 'Numéro de téléphone',
            'assigned_unit': 'Unité assignée',
            'user': 'Utilisateur'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'placeholder': 'Nom complet'}),
            'role': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'placeholder': 'Numéro de téléphone'}),
            'assigned_unit': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black'}),
            'user': forms.HiddenInput(),  # Hide the user field as it will be set automatically
        }

class SupportStaffForm(forms.ModelForm):
    class Meta:
        model = SupportStaff
        fields = '__all__'
        labels = {
            'name': 'Nom complet',
            'role': 'Rôle',
            'email': 'Email',
            'phone_number': 'Numéro de téléphone',
            'assigned_unit': 'Unité assignée'
        }

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'quantity', 'unit']
        labels = {
            'name': 'Nom de l\'équipement',
            'quantity': 'Quantité',
            'unit': 'Unité'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'placeholder': 'Nom de l\'équipement'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'min': '0', 'placeholder': 'Quantité'}),
            'unit': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black'}),
        }

class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = '__all__'
        labels = {
            'unit': 'Unité',
            'date': 'Date',
            'location': 'Localisation',
            'description': 'Description',
            'patients_treated': 'Patients traités',
            'status': 'Statut'
        }
        widgets = {
            'unit': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black'}),
            'location': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'placeholder': 'Lieu de l\'intervention'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'placeholder': 'Description de l\'intervention'}),
            'patients_treated': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'min': '0', 'placeholder': 'Nombre de patients traités'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter units to only show active ones
        self.fields['unit'].queryset = MobileUnit.objects.filter(
            status='active'
        ).order_by('name')

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender',
            'phone_number', 'address', 'medical_history', 'allergies',
            'blood_type'
        ]
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'date_of_birth': 'Date de naissance',
            'gender': 'Genre',
            'phone_number': 'Numéro de téléphone',
            'address': 'Adresse',
            'medical_history': 'Antécédents médicaux',
            'allergies': 'Allergies',
            'blood_type': 'Groupe sanguin'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'placeholder': 'Nom'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black'}),
            'gender': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'placeholder': 'Numéro de téléphone'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'placeholder': 'Adresse'}),
            'medical_history': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'placeholder': 'Antécédents médicaux'}),
            'allergies': forms.Textarea(attrs={'rows': 2, 'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'placeholder': 'Allergies'}),
            'blood_type': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'placeholder': 'Groupe sanguin'}),
        }

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['doctor', 'unit', 'diagnosis', 'treatment', 'notes']
        labels = {
            'doctor': 'Médecin',
            'unit': 'Unité',
            'diagnosis': 'Diagnostic',
            'treatment': 'Traitement',
            'notes': 'Notes'
        }
        widgets = {
            'doctor': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black'}),
            'unit': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black'}),
            'diagnosis': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'placeholder': 'Diagnostic'}),
            'treatment': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'placeholder': 'Traitement'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black', 'placeholder': 'Notes additionnelles'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter units to show only active ones
        self.fields['unit'].queryset = MobileUnit.objects.filter(status='active')
        
        # If user is provided and is medical staff, filter doctors and set unit
        if user and hasattr(user, 'medicalstaff'):
            medical_staff = user.medicalstaff
            if medical_staff.assigned_unit:
                # Set the unit to the staff's assigned unit
                self.fields['unit'].initial = medical_staff.assigned_unit
                self.fields['unit'].widget.attrs['readonly'] = True
                
                # Filter doctors to show only those from the same unit and get their user instances
                self.fields['doctor'].queryset = User.objects.filter(
                    medicalstaff__assigned_unit=medical_staff.assigned_unit,
                    medicalstaff__role='doctor'
                )
            else:
                # If no unit assigned, disable the form
                for field in self.fields:
                    self.fields[field].widget.attrs['disabled'] = True
                self.fields['unit'].widget.attrs['readonly'] = True
                self.fields['unit'].initial = None
                self.fields['doctor'].queryset = User.objects.none()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Nom d\'utilisateur',
            'email': 'Email',
            'password1': 'Mot de passe',
            'password2': 'Confirmer le mot de passe'
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Email'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-black'}),
        }