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
        'first_name',
        'last_name',
        'phone_number',
        'major',
        'graduation_year',
        'gpa',
        'view_cv_document',
        'is_available',
    )
    list_filter = ('major__name','graduation_year','is_available')
    search_fields = ('first_name','phone_number','graduation_year','gpa')
    list_editable = ('is_available',)
    exclude = ['user']

    def view_cv_document(self, obj):
        if obj.cv_file:
            return format_html(
                '<a href="{}" target="_blank" style="color: #2563eb; text-decoration: underline;">{}</a>',
                obj.cv_file.url, _("View Document"))
        return _("No Document")

    view_cv_document.short_description = _("CR Document")

