from django.contrib import admin
from django.utils.html import format_html
from core.admin import BaseModelAdmin
from students.models import StudentProfile
from django.utils.translation import gettext_lazy as _

# Register your models here.

@admin.register(StudentProfile)
class StudentProfileAdmin(BaseModelAdmin):
    tailwind_fields = []
    list_display = (
        'user',
        'first_name',
        'last_name',
        'phone_number',
        'major',
        'get_university',
        'graduation_year',
        'gpa',
        'view_cv_file',
        'is_available',
    )
    list_filter = ('is_available','graduation_year','major__college__university',)
    search_fields = ('first_name','phone_number','graduation_year','gpa')
    list_editable = ('is_available',)
    exclude = ['user']

    def get_university(self, obj):
        if obj.major and obj.major.college and obj.major.college.university:
            return obj.major.college.university
        return "-"

    def view_cv_file(self, obj):
        if obj.cv_file:
            return format_html(
                '<a href="{}" target="_blank" style="color: #2563eb; text-decoration: underline;">{}</a>',
                obj.cv_file.url, _("View CV File"))
        return _("No CV File")


    get_university.short_description = 'University'  # تحديد الاسم الذي سيظهر في رأس الجدول
    get_university.admin_order_field = 'major__college__university'     # # اختياري: لجعل العمود قابلاً للترتيب في الجدول
    view_cv_file.short_description = _("CV File")

