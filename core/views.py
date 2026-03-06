# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser

def home(request):
    return render(request, 'core/home.html')

@login_required
def toggle_theme(request):
    user = request.user
    user.is_dark_mode = not user.is_dark_mode
    user.save()
    return JsonResponse({'status': 'success', 'is_dark_mode': user.is_dark_mode})

@login_required
def search_users(request):
    query = request.GET.get('search', '') # تأكد أن name="search" في الـ input
    if query:
        users = CustomUser.objects.filter(username__icontains=query)
    else:
        users = []

    # التغيير هنا: نرسل قالب النتائج فقط
    return render(request, 'core/partials/user_list_results.html', {'users': users})