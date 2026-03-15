from django.urls import path
from . import views

# هذا السطر هو الذي يحل مشكلة الـ Namespace
app_name = 'academy'

urlpatterns = [

    path('load-universities/', views.load_universities, name='load_universities'),
    path('load-colleges/', views.load_colleges, name='load_colleges'),
    path('load-majors/', views.load_majors, name='load_majors'),
]