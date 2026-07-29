from django.urls import path
from . import views

# هذا السطر هو الذي يحل مشكلة الـ Namespace
app_name = 'students'

urlpatterns = [
    # تأكد أن اسم الـ name هو 'dashboard' ليطابق قاموس التوجيه لديك
    path('dashboard/', views.dashboard, name='dashboard'),
    path('complete-profile/', views.student_complete_profile, name='complete_profile'),


    # path('ajax/load-colleges/', views.load_colleges, name='ajax_load_colleges'),
    # path('ajax/load-majors/', views.load_majors, name='ajax_load_majors'),

    path('match-opportunities/', views.match_opportunities, name='match_opportunities'),
    path('my-opportunities-apps/', views.my_opportunities_apps, name='my_opportunities_apps'),
    path('opportunities/invites', views.opportunities_invitations, name='opportunities_invites'),
    path('opportunity/<int:id>/detail/', views.opportunity_detail, name='opportunity_detail'),
    path('opportunity/<int:opportunity_id>/join/', views.opportunity_apply, name='opportunity_apply'),




]