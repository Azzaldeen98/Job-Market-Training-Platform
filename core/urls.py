from django.urls import path

from accounts.views import waiting_approval_view
from . import views

app_name = 'core'

# تأكد أن الاسم urlpatterns بالجمع (s في النهاية) وكل الحروف small
urlpatterns = [
    path('', views.home, name='home'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('search/', views.search_users, name='search_users'),
    path('training-entity-profile/<int:id>/view/', views.training_entity_profile_view, name='training_entity_profile_view'),
    path('training-entities/index/', views.training_entities, name='training_entities'),
    path('opportunity/<int:id>/view/', views.opportunity_detail, name='opportunity_view'),
    path('opportunity/index', views.opportunities, name='opportunities'),

    path('load_countries/', views.load_countries, name='load_countries'),
    # path('add_country/', views.add_country, name='add_country'),
]