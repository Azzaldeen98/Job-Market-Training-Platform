from django import forms
from django.core.exceptions import ValidationError

from academy.models import College, Major, University


class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name', 'city','type']

class CollegeForm(forms.ModelForm):
    class Meta:
        model = College
        fields = ['name', 'university']

class MajorForm(forms.ModelForm):
    class Meta:
        model = Major
        fields = ['name', 'description','college']