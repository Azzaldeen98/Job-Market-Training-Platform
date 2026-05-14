from django.urls import path
from . import views


app_name = 'applications'

urlpatterns = [

    path('join/<int:opportunity_id>/', views.join_opportunity, name='join_opportunity'),
    path('opportunity/<int:opportunity_id>/cancel/', views.cancel_join_opportunity, name='cancel_app_opportunity'),
    path('application_review/<int:application_id>/', views.view_application_details, name='application_review'),
]