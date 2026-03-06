from django.urls import path
from . import views

app_name = 'core'

# تأكد أن الاسم urlpatterns بالجمع (s في النهاية) وكل الحروف small
urlpatterns = [
    path('', views.home, name='home'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('search/', views.search_users, name='search_users'),
]