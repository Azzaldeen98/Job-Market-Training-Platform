from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import College, Major, University, Skill


def load_universities(request):
    # city_id = request.GET.get('city')
    universities = University.objects.all().order_by('name')
    return render(request, 'academy/partials/university_options.html', {'universities': universities})

def load_colleges(request):
    university_id = request.GET.get('university')
    colleges = College.objects.filter(university_id=university_id).order_by('name')
    return render(request, 'academy/partials/college_options.html', {'colleges': colleges})

def load_majors(request):
    college_id = request.GET.get('college')
    majors = Major.objects.filter(college_id=college_id).order_by('name')
    return render(request, 'academy/partials/major_options.html', {'majors': majors})

def load_skills(request):

    category_skills = Skill.objects.all().order_by('name')
    return render(request, 'academy/partials/category_skill_options.html', {'category_skills': category_skills})

def load_skills(request):
    category_id = request.GET.get('category')
    skills = Skill.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'academy/partials/skill_options.html', {'skills': skills})