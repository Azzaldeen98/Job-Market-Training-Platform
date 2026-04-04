from django.urls import path
from . import views


app_name = 'applications'

urlpatterns = [

    path('join/<int:opportunity_id>/', views.join_opportunity, name='join_opportunity'),
    path('application_review/<int:application_id>/', views.view_application_details, name='application_review'),
]