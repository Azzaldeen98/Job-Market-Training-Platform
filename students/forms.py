from django import forms
from django.core.exceptions import ValidationError
import datetime

from academy.models import Major, College, University
from core.constants import FormErrorMessages as MSG
from core.forms import CoreModelForm
from core.validators import PhoneValidator
from students.models import StudentProfile
from django.utils.translation import gettext_lazy as _

class StudentProfileForm(CoreModelForm):

    current_year = datetime.date.today().year

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(validators=[PhoneValidator(prefix='05', length=10)]
                                   ,required=True)
    
    gpa = forms.CharField(required=True)


    university = forms.ModelChoiceField(queryset=University.objects.all(), required=True,
                                        widget=forms.Select(attrs={'id': 'id_university'}))
    college = forms.ModelChoiceField(queryset=College.objects.all(), required=True,
                                     widget=forms.Select(attrs={'id': 'id_college', 'disabled': 'disabled'}))
    major = forms.ModelChoiceField(queryset=Major.objects.all(), required=True,
                                   widget=forms.Select(attrs={'id': 'id_major', 'disabled': 'disabled'}))
    graduation_year = forms.TypedChoiceField(
        coerce=int,
        choices=[(year, str(year)) for year in range(current_year - 10, current_year+7 )],
        required=True,
        label=_("Graduation Year"),
        error_messages={
            'invalid': 'Please enter a valid year.',
            'min_value': 'Graduation year is too old.',
            'max_value': 'Graduation year is too far in the future.',
        }
    )

    picture = forms.ImageField(required=False)
    cv_file = forms.FileField(required=False)


    class Meta:
        model= StudentProfile

        fields=('first_name', 'last_name','phone_number', 'university', 'college','major', 'graduation_year',
            'gpa','skills','picture', 'cv_file')

        widgets = {
            'graduation_year': forms.NumberInput(attrs={'placeholder': '2026'}),
            'gpa': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '4.00'}),
            'skills': forms.SelectMultiple(attrs={'class': 'select2-enable '}),  # إذا كنت تستخدم مكتبة Select2
        }

        error_messages = {
            'phone_number': {
                'phone_start': MSG.PHONE_START,
                'phone_length': MSG.PHONE_LEN,
            },
            'graduation_year': {
                'invalid_year': MSG.GRADUATION_YEAR,
            },
            'gpa': {
                'out_of_range':MSG.GPA_OUT_RANGE ,
            }  ,
            'picture': {
                'file_too_large': _("CV file size must be under 2MB.") ,
                'invalid_extension': MSG.INVALID_PDF_EXTENSION,
            } ,
            'cv_file': {
                'image_too_large': _("Image file too large (Max 1MB)") ,
                'invalid_image_format': _("Unsupported file extension. Use JPG or PNG.") ,
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        # إجبار المستخدم على اختيار التخصص في الواجهة
        self.fields['major'].required = True
        self.fields['major'].empty_label = _("Choose your academic major")

        for field_name, field in self.fields.items():
            # 1. الحفاظ على أي كلاسات تمت إضافتها يدوياً في الـ widgets
            existing = field.widget.attrs.get('class', '')
            # 3. دمج الكلاسات وتحديث الحقل
            if field_name!='skills':
                field.widget.attrs['class'] = f"{existing}  bg-gray-700  max-w-md".strip()

    def clean_phone_number(self):
        clean_data=super().clean()
        phone=clean_data.get('phone_number')
        if not phone.startswith('05'):
            raise forms.ValidationError(
                self.fields['phone_number'].error_messages['phone_start']
            )
        # Additional length requirement (optional but professional)
        if len(phone) != 10:
            raise forms.ValidationError(
                self.fields['phone_number'].error_messages['phone_length']
            )
        return phone
    def clean_picture(self):
        picture = self.cleaned_data.get('picture')
        if picture:
            # 1. التحقق من الحجم (مثلاً: حد أقصى 1 ميجابايت)
            if picture.size > 1 * 1024 * 1024:
                raise forms.ValidationError(
                    self.fields['picture'].error_messages['image_too_large'],
                    code='image_too_large'
                )

            # 2. التحقق من الامتداد (اختياري لأن ImageField يفعل ذلك جزئياً)
            extension = picture.name.split('.')[-1].lower()
            if extension not in ['jpg', 'jpeg', 'png']:
                raise forms.ValidationError(
                    self.fields['picture'].error_messages['invalid_image_format'],
                    code='invalid_image_format' )
        return picture

    def clean_graduation_year(self):
        """التحقق من سنة التخرج"""
        year = self.cleaned_data.get('graduation_year')
        from datetime import date
        current_year = date.today().year

        if year:

            if year > current_year:
                raise forms.ValidationError(
                    self.fields['graduation_year'].error_messages['max_value'],
                    code='future_year'
                )
            elif year < current_year - 10:
                raise forms.ValidationError(
                    self.fields['graduation_year'].error_messages['min_value'],
                    code='past_year'
                )

        return year

    def clean_gpa(self):
        """التحقق من المعدل التراكمي"""
        gpa = self.cleaned_data.get('gpa')
        if gpa is not None:
            if gpa < 0 or gpa > 5.00 : # or gpa > 4.00 or  gpa > 100.0:
                raise forms.ValidationError(
                    self.fields['gpa'].error_messages['out_of_range'],
                    code='invalid_gpa'
                )
        return gpa

    def clean_cv_file(self):
        """التحقق من صيغة ملف السيرة الذاتية وحجمه"""
        cv = self.cleaned_data.get('cv_file')
        if cv:
            # التحقق من الحجم (مثلاً لا يتجاوز 2MB)
            if cv.size > 2 * 1024 * 1024:
                raise forms.ValidationError(
                self.fields['cv_file'].error_messages['file_too_large'],
                 code='file_too_large')
            # التحقق من الامتداد
            if not cv.name.endswith('.pdf'):
                raise forms.ValidationError(
                self.fields['cv_file'].error_messages['invalid_extension'],
                 code='invalid_extension')
        return cv
