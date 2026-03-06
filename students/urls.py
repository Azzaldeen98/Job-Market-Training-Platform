from django.urls import path
from . import views

# هذا السطر هو الذي يحل مشكلة الـ Namespace
app_name = 'students'

urlpatterns = [
    # تأكد أن اسم الـ name هو 'dashboard' ليطابق قاموس التوجيه لديك
    path('dashboard/', views.dashboard, name='dashboard'),
]