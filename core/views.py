# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .models import Region, City
from .forms import CountryForm, RegionForm, CityForm

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


#=======================================================================================================

#
# @login_required
# def add_country(request):
#     if request.method == "POST":
#         form = CountryForm(request.POST)
#         if form.is_valid():
#             country = form.save()
#             # نرسل الدولة الجديدة للقالب لتحديث قائمة الـ Select
#             # لاحظ أننا وضعناها في قائمة [country] لتجنب أخطاء الـ loop في القالب
#             return render(request, 'core/partials/country_options.html', {'countries': [country]})
#     else:
#         form = CountryForm()
#
#     return render(request, 'core/partials/country_form_modal.html', {'form': form})
#
# # locations/views.py
#
# @login_required
# def add_region(request):
#     # جلب الدولة المختارة من الرابط (Query Params) إن وجدت
#     selected_country_id = request.GET.get('country')
#
#     if request.method == "POST":
#         form = RegionForm(request.POST)
#         if form.is_valid():
#             region = form.save()
#             return render(request, 'core/partials/region_options.html', {'regions': [region]})
#     else:
#         # تمرير الدولة كقيمة ابتدائية للفورم
#         initial_data = {}
#         if selected_country_id:
#             initial_data['country'] = selected_country_id
#
#         form = RegionForm(initial=initial_data)
#
#     return render(request, 'core/partials/region_form_modal.html', {'form': form})
#
# @login_required
# def add_city(request):
#     # جلب الدولة المختارة من الرابط (Query Params) إن وجدت
#     selected_region_id = request.GET.get('region')
#
#     if request.method == "POST":
#         form = CityForm(request.POST)
#         if form.is_valid():
#             city = form.save()
#             return render(request, 'core/partials/city_options.html', {'cities': [city]})
#     else:
#         # تمرير الدولة كقيمة ابتدائية للفورم
#         initial_data = {}
#         if selected_region_id:
#             initial_data['region'] = selected_region_id
#
#         form = CityForm(initial=initial_data)
#
#     return render(request, 'core/partials/city_form_modal.html', {'form': form})

#=======================================================================================================

def load_countries(request):

    countries = Region.objects.all().order_by('name')
    return render(request, 'core/partials/country_options.html', {'countries': countries})

def load_regions(request):
    country_id = request.GET.get('country')
    regions = Region.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'core/partials/region_options.html', {'regions': regions})

def load_cities(request):
    region_id = request.GET.get('region')
    cities = City.objects.filter(region_id=region_id).order_by('name')
    return render(request, 'locations/partials/city_options.html', {'cities': cities})