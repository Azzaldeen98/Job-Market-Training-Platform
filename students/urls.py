from django.urls import path
from . import views

# هذا السطر هو الذي يحل مشكلة الـ Namespace
app_name = 'students'

urlpatterns = [
    # تأكد أن اسم الـ name هو 'dashboard' ليطابق قاموس التوجيه لديك
    path('dashboard/', views.dashboard, name='dashboard'),
    path('complete-profile/', views.student_complete_profile, name='complete_profile'),
    path('match-opportunities/', views.match_opportunities, name='match_opportunities'),
    path('opportunity/<int:id>/', views.opportunity_detail, name='opportunity_detail'),
    # path('opportunity/<int:opportunity_id>/join/', views.join_opportunity, name='join_opportunity'),
]