from django.urls import path
from . import views

# هذا السطر هو الذي يحل مشكلة الـ Namespace
app_name = 'training_entities'

urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),
    path('complete_profile/', views.training_entity_complete_profile, name='complete_profile'),


    # Loading Data
    path('ajax/load-universities/', views.load_universities, name='ajax_load_universities'),
    path('ajax/load-colleges/', views.load_colleges, name='ajax_load_colleges'),
    path('ajax/load-majors/', views.load_majors, name='ajax_load_majors'),

    # Training Opportunities
    path('training_opportunities/', views.opportunities_list, name='training_opportunities'),
    path('training_opportunity/view/<int:id>/', views.opportunity_detail, name='opportunity_detail'),
    path('incoming_apps/', views.incoming_apps, name='incoming_apps'),

    path('applicant/<int:app_id>/accept', views.applicant_acceptance, name='applicant_accept'),
    path('applicant/<int:app_id>/rejected', views.applicant_rejected, name='applicant_rejected'),
    path('applicant/<int:app_id>/on_training', views.applicant_on_training, name='applicant_on_training'),
    path('applicant/<int:app_id>/completed', views.applicant_completed, name='applicant_completed'),
    # path('applicant/<int:app_id>/cancel', views.applicant_completed, name='applicant_completed'),

    path('training_opportunity/apps/<int:id>/', views.opportunity_apps, name='opportunity_apps'),
    path('training_opportunity/add/', views.training_opportunity, name='opportunity_add'),
    path('training_opportunity/edit/<int:id>/', views.training_opportunity, name='opportunity_edit'),
    path('training_opportunity/delete/<int:id>/', views.delete_opportunity, name='opportunity_delete'),
    # match
    path('check-match/<int:opportunity_id>/', views.check_match, name='check_match'),

    # path('student_profile/<int:student_id>/', views.student_profile, name='student_profile'),
    path('student_profile', views.student_profile, name='student_profile'),

    path('send_invite/<int:opportunity_id>/<int:student_id>/', views.send_invite, name='send_invite'),
    path('cancel_invite/<int:opportunity_id>/<int:student_id>/', views.cancel_invite, name='cancel_invite'),

]