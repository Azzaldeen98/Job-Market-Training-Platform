from django.urls import path
from . import views

# هذا السطر هو الذي يحل مشكلة الـ Namespace
app_name = 'training_entities'

urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),
    path('complete_profile/', views.training_entity_complete_profile, name='complete_profile'),
    # Loading Data
    path('ajax/load-colleges/', views.load_colleges, name='ajax_load_colleges'),
    path('ajax/load-majors/', views.load_majors, name='ajax_load_majors'),

    # Training Opportunities
    path('training_opportunities/', views.opportunities_list, name='training_opportunities'),
    path('training_opportunity/view/<int:id>/', views.opportunity_detail, name='opportunity_detail'),
    path('training_opportunity/add/', views.training_opportunity, name='opportunity_add'),
    path('training_opportunity/edit/<int:id>/', views.training_opportunity, name='opportunity_edit'),
    path('training_opportunity/delete/<int:id>/', views.delete_opportunity, name='opportunity_delete'),
    # match
    path('check-match/<int:opportunity_id>/', views.check_match, name='check_match'),
]