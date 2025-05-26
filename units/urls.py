from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('units/', views.unit_list, name='unit_list'),
    path('units/create/', views.unit_create, name='unit_create'),
    path('units/<int:unit_id>/update/', views.unit_update, name='unit_update'),
    path('units/<int:unit_id>/delete/', views.unit_delete, name='unit_delete'),
    path('units/<int:pk>/', views.unit_detail, name='unit_detail'),
    path('units/<int:unit_id>/tracking/', views.unit_tracking, name='unit_tracking'),
    path('units/<int:unit_id>/update-location/', views.update_unit_location, name='update_unit_location'),
    path('units/calendar/', views.unit_calendar, name='unit_calendar'),
    
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/<int:staff_id>/', views.staff_detail, name='staff_detail'),
    path('staff/create/', views.staff_create, name='staff_create'),
    path('staff/<int:staff_id>/update/', views.staff_update, name='staff_update'),
    path('staff/<int:staff_id>/delete/', views.staff_delete, name='staff_delete'),
    
    path('support/', views.support_list, name='support_list'),
    path('support/create/', views.support_create, name='support_create'),
    path('support/<int:support_id>/update/', views.support_update, name='support_update'),
    path('support/<int:support_id>/delete/', views.support_delete, name='support_delete'),
    
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/create/', views.equipment_create, name='equipment_create'),
    path('equipment/<int:equipment_id>/update/', views.equipment_update, name='equipment_update'),
    path('equipment/<int:equipment_id>/delete/', views.equipment_delete, name='equipment_delete'),
    path('equipment/<int:equipment_id>/', views.equipment_detail, name='equipment_detail'),
    
    path('interventions/', views.intervention_list, name='intervention_list'),
    path('interventions/create/', views.intervention_create, name='intervention_create'),
    path('interventions/<int:intervention_id>/', views.intervention_detail, name='intervention_detail'),
    path('interventions/<int:intervention_id>/update/', views.intervention_update, name='intervention_update'),
    path('interventions/<int:intervention_id>/delete/', views.intervention_delete, name='intervention_delete'),
    
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/create/', views.patient_create, name='patient_create'),
    path('patients/<uuid:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patients/<uuid:patient_id>/update/', views.patient_update, name='patient_update'),
    path('patients/<uuid:patient_id>/delete/', views.patient_delete, name='patient_delete'),
    path('patients/<uuid:patient_id>/medical-records/create/', views.medical_record_create, name='medical_record_create'),
    path('medical-records/<int:record_id>/', views.medical_record_detail, name='medical_record_detail'),
    path('medical-records/<int:record_id>/update/', views.medical_record_update, name='medical_record_update'),
    
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('users/', views.user_list, name='user_list'),
    
    # URLs pour la gestion du mot de passe
    path('password/change/', auth_views.PasswordChangeView.as_view(
        template_name='units/password_change.html',
        success_url='/dashboard/profile/'
    ), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='units/password_change_done.html'
    ), name='password_change_done'),
    
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    path('reports/', views.reports_dashboard, name='reports_dashboard'),
    
    path('api/units/<int:unit_id>/doctors/', views.get_unit_doctors, name='get_unit_doctors'),
    path('units/<int:unit_id>/report/', views.generate_unit_report, name='unit_report'),
]
