from django import forms
from django.utils.translation import gettext_lazy as _

from academy.models import Major, University, College
from core.forms import CoreModelForm
from core.validators import FileValidator, PhoneValidator
from training_entities.models import TrainingEntityProfile, TrainingOpportunity


class TrainingEntityProfileForm(CoreModelForm):

    # validation

    image_validator = FileValidator( max_size_mb=1, allowed_extensions=['jpg', 'png', 'jpeg'],)
    doc_validator = FileValidator(max_size_mb=2, allowed_extensions=['pdf'])
    saudi_phone_rules = PhoneValidator(prefix='05', length=10)

    phone_number = forms.CharField(validators=[saudi_phone_rules])
    logo = forms.ImageField(validators=[image_validator])
    cover_image = forms.ImageField(validators=[image_validator])
    commercial_register = forms.FileField(validators=[doc_validator])

    class Meta:
        model= TrainingEntityProfile

        fields=('entity_name','entity_type', 'description','city','phone_number', 'registration_number',
            'logo', 'cover_image', 'commercial_register', 'website')

        widgets = {
            'entity_name': forms.TextInput(attrs={'placeholder': _('Enter training entity name')}),
            'entity_type': forms.Select(attrs={'class': 'form-select','placeholder': _("Select the legal status of your organization")}),
            'description': forms.Textarea(attrs={
                'placeholder': _('Brief description about the training entity...'),
                'rows': 4
            }),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'phone_number': forms.TextInput(attrs={'placeholder': _('05xxxxxxxx')}),
            'registration_number': forms.TextInput(attrs={'placeholder': _('Commercial Registration No.')}),
            'website': forms.URLInput(attrs={'placeholder': _('https://example.com')}),

            # حقول الملفات والصور تستخدم FileInput للتحكم في الـ HTML
            'logo': forms.FileInput(attrs={'class': 'file-input'}),
            'cover_image': forms.FileInput(attrs={'class': 'file-input'}),
            'commercial_register': forms.FileInput(attrs={'class': 'file-input'}),
        }

        # exclude = ['is_available']



        #
        # error_messages = {
        #     'phone_number': {
        #         'phone_start': _(MSG.PHONE_START),
        #         'phone_length': _(MSG.PHONE_LEN),
        #     },
        #     'graduation_year': {
        #         'invalid_year': _(MSG.GRADUATION_YEAR),
        #     },
        #     'gpa': {
        #         'out_of_range':_(MSG.GPA_OUT_RANGE) ,
        #     }  ,
        #     'picture': {
        #         'file_too_large': _("CV file size must be under 2MB.") ,
        #         'invalid_extension': _(MSG.INVALID_PDF_EXTENSION) ,
        #     } ,
        #     'cv_file': {
        #         'image_too_large': _("Image file too large (Max 1MB)") ,
        #         'invalid_image_format': _("Unsupported file extension. Use JPG or PNG.") ,
        #     }
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # إجبار المستخدم على اختيار التخصص في الواجهة
        self.fields['city'].required = True
        self.fields['city'].empty_label = _("Choose City ")


class TrainingOpportunityForm(CoreModelForm):



    # validation
    # start_date=forms.DateInput(attrs={'type': 'date',})
    # end_date=forms.DateInput(attrs={'type': 'date',})
    # deadline=forms.DateInput(attrs={'type': 'date',})

    university = forms.ModelChoiceField(queryset=University.objects.all(), required=False,widget=forms.Select(attrs={'id': 'id_university'}))
    college = forms.ModelChoiceField(queryset=College.objects.all(), required=False, widget=forms.Select(attrs={'id': 'id_college', 'disabled': 'disabled'}))
    major = forms.ModelChoiceField(queryset=Major.objects.all(), widget=forms.Select(attrs={'id': 'id_major', 'disabled': 'disabled'}))

    class Meta:
        model= TrainingOpportunity
        #'description,'status','provider', 'majors'
        fields=('title','city','start_date', 'end_date',
            'deadline', 'capacity','gpa_scale','min_gpa','required_skills',
            'university', 'college','major',
            'benefits','other_skills_notes','additional_requirements')

        widgets = {
            'start_date': forms.DateInput(attrs={ 'type': 'date', }),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'deadline': forms.DateInput(attrs={ 'type': 'date',}),
            'required_skills': forms.SelectMultiple(attrs={'class': 'select2-enable'}),

        }
        # exclude = ['is_available']

    # def clean_required_skills(self):
    #     skills = self.cleaned_data.get('required_skills')
    #     if isinstance(skills, list):
    #         return ", ".join(skills)  # تحويل ['A', 'B'] إلى "A, B"
    #     return skills

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['city'].required = True
        self.fields['city'].empty_label = _("Choose City")



        if self.instance and self.instance.pk:
            # --- منطق التخصصات (كودك الحالي) ---
            selected_major = self.instance.major
            if selected_major:
                college = selected_major.college
                university = college.university
                self.initial['university'] = university
                self.initial['college'] = college
                self.initial['major'] = selected_major
                self.fields['college'].queryset = College.objects.filter(university=university)
                self.fields['major'].queryset = Major.objects.filter(college=college)
                self.fields['college'].widget.attrs.pop('disabled', None)
                # self.fields['major'].widget.attrs.pop('disabled', None)

            # منطق المهارات: تحويلها لنص ليقرأها الـ JavaScript
            # جلب المهارات المرتبطة وتحويلها لنص
            # print(f"--- Debug: Editing Opportunity ID: {self.instance} ---")
            #
            # # جلب المهارات
            # skills_qs = self.instance.required_skills.all()
            #
            # # طباعة الـ QuerySet نفسه
            # print(f"--- Debug: Skills QuerySet: {len(skills_qs)} ---")
            #
            # # طباعة الأسماء المستخرجة (إذا وجدت)
            # if skills_qs.exists():
            #     skills_names = ", ".join([s.name for s in skills_qs])
            #     print(f"--- Debug: Skills Names String: {skills_names} ---")
            #
            #     # حقن القيمة (الكود الذي نحاول إصلاحه)
            #     self.fields['required_skills'].widget.attrs['data-current-skills'] = skills_names
            #     self.initial['required_skills'] = skills_names
            # else:
            #     print("--- Debug: No skills found for this instance in Database ---")


# class TrainingOpportunities: