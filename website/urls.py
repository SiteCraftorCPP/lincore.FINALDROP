from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    path('documents/personal-data/', views.personal_data_policy, name='personal_data_policy'),
    
    # Страницы услуг
    path('services/complex/', views.complex_service, name='complex_service'),
    path('services/heating/', views.heating_service, name='heating_service'),
    path('services/verification/', views.verification, name='verification'),
    path('services/emergency/', views.emergency, name='emergency'),
    path('services/installation/', views.installation, name='installation'),
    path('services/audit/', views.audit, name='audit'),
    path('services/heating-preparation/', views.heating_preparation, name='heating_preparation'),
    path('services/ventilation/', views.ventilation, name='ventilation'),
    
    # AJAX для форм
    path('ajax/service-application/', views.service_application, name='service_application'),
    path('ajax/tender-invitation/', views.tender_invitation, name='tender_invitation'),
    path('submit-request/', views.submit_request, name='submit_request'),
    path('submit-quote/', views.submit_quote, name='submit_quote'),
    
    
]
