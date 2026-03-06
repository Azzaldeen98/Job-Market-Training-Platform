
from django.urls import path
from django.contrib.auth import views as auth_views
# from . import views
from django.urls import path, include
from .views import redirect_by_role,signup

app_name = 'accounts'

urlpatterns = [
    path('register/', signup, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # views يمثل ملف views.py حيث يمكننا الوصول الى الفئات او الدوال التي بداخله
    path('signup/', signup, name='signup'),
    path('redirect-by-role/', redirect_by_role, name='redirect_by_role'),
]