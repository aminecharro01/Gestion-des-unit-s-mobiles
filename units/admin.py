from django.contrib import admin
from .models import MobileUnit, MedicalStaff, SupportStaff, Equipment, Intervention, Patient

admin.site.register(MobileUnit)
admin.site.register(MedicalStaff)
admin.site.register(SupportStaff)
admin.site.register(Equipment)
admin.site.register(Intervention)
admin.site.register(Patient)
