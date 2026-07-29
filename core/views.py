# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from academy.models import College,Major
from accounts.models import CustomUser
from applications.models import JoinTrainingOpportunity
from students.models import StudentProfile
from training_entities.models import TrainingOpportunity, TrainingEntityProfile
from .models import Region, City
from django.db.models import Count
from .forms import CountryForm, RegionForm, CityForm
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from .routes import Routes
from .utils import calculate_match_score, current_date
# views.py
from django.http import JsonResponse


# def get_colleges(request):
#     university_id = request.GET.get('university_id')
#     colleges = College.objects.filter(university_id=university_id).values('id', 'name')
#     return JsonResponse(list(colleges), safe=False)
#
# def get_majors(request):
#     college_id = request.GET.get('college_id')
#     majors = Major.objects.filter(college_id=college_id).values('id', 'name')
#     return JsonResponse(list(majors), safe=False)

def home(request):
    most_active_entities = TrainingEntityProfile.objects.filter(is_available=True,user__is_active=True).annotate(
        opportunities_count=Count('opportunities')

    ).exclude(entity_name="")[:4]

    context = {
        "companies_count": TrainingEntityProfile.objects.count(),
        "students_count": StudentProfile.objects.count(),
        "opportunities_count": TrainingOpportunity.objects.count(),
        "apps_count": JoinTrainingOpportunity.objects.count(),
        "most_active_entities": most_active_entities,
        "opportunities": opportunities,
    }


    return render(request, 'core/home.html',context)

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


@login_required
def search_opportunities(request):
    query = request.GET.get('search', '').strip()

    if query:
        opportunities = TrainingOpportunity.objects.filter(
            status='open',
            provider__is_available=True)\
            .filter(
                Q(title__icontains=query) |
                Q(provider__entity_name__icontains=query) |
                Q(required_skills__name__icontains=query) |
                Q(major__name__icontains=query)
        ).distinct()
    else:

        opportunities = TrainingOpportunity.objects.filter(status='open',provider__is_available=True)

    return render(request, 'core/partials/opportunities.html', {'opportunities': opportunities})


@login_required
def training_entity_profile_view(request,id):
    entity = get_object_or_404(TrainingEntityProfile, id=id)
    return render(request, 'core/training_entity_profile_view.html', {'entity': entity})

# @login_required
def training_entities(request):

    entities = TrainingEntityProfile.objects.filter(is_available=True,user__is_active=True).exclude(entity_name="")

    return render(request, f'core/training_entities.html', {
        "entities":entities
    })

def opportunity_detail(request,id):


    opportunity = get_object_or_404(TrainingOpportunity, id=id)

    has_applied = False
    matching_result =  0

    if request.user.is_authenticated :

        if not request.user.profile.is_profile_complete:
            return redirect(Routes.STUDENT_COMPLETE_PROFILE)

        student = get_object_or_404(StudentProfile, user=request.user)

        if (student and opportunity):

            has_applied = JoinTrainingOpportunity.objects.filter(student=student, opportunity=opportunity).exists()
            matching_result =  calculate_match_score(student, opportunity)


    context = {
        'matching_result': matching_result,
        'opportunity': opportunity,
        'has_applied': has_applied,
    }

    return render(request, f'core/opportunities/opportunity_detail.html', context)


def opportunities(request):
    # student=None
    today = current_date()
    results = []

    # if request.user.is_authenticated:
    #
    #     student = get_object_or_404(StudentProfile, user=request.user)
    #
    #     if not request.user.profile.is_profile_complete:
    #         return redirect(Routes.STUDENT_COMPLETE_PROFILE)
    #     else:
    #
    #         query = Q(end_date__gte=today) & (Q(major=student.major) | Q(major__isnull=True))
    #         if student.gpa is not None:
    #             query &= (Q(min_gpa__lte=student.gpa) | Q(min_gpa__isnull=True))
    #         else:
    #             query &= Q(min_gpa__isnull=True)
    #
    #         potential_opportunities = TrainingOpportunity.objects.filter(query) \
    #             .prefetch_related('required_skills', 'provider').distinct()
    #
    #         for opp in potential_opportunities:
    #
    #             application = JoinTrainingOpportunity.objects.filter(student=student, opportunity=opp).first()
    #             std_opp_status = None
    #             if application:
    #                 std_opp_status = application.status
    #
    #             match_percent = calculate_match_score(student, opp)
    #
    #             # if match_percent > 30:
    #             results.append({
    #                 'opportunity': opp,
    #                 'status': std_opp_status,
    #                 'score': round(match_percent, 1)
    #             })
    #
    #         results.sort(key=lambda x: x['score'], reverse=True)
    # else:

    potential_opportunities = TrainingOpportunity.objects.filter(Q(end_date__gte=today)) \
        .prefetch_related('required_skills', 'provider').distinct()

    for opp in potential_opportunities:
        results.append({
                        'opportunity': opp,
                        'status': None,
                        'score': 0
                    })

    # print("results:",len(results))
    # print(results)

    return render(request,
                  f'core/opportunities/opportunity_list.html', {
                      'results': results,
                  })





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