from django.contrib import admin
from core.admin import BaseModelAdmin
from training_entities.models import TrainingEntityProfile, Industry
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.
@admin.register(TrainingEntityProfile)
class TrainingEntityProfileAdmin(BaseModelAdmin):
    tailwind_fields = []

    list_display = (
        'view_logo',
        'entity_name',
        'entity_type',
        'description',
        'phone_number',
        'city',
        'view_cr_document',
        'is_available',
    )
    list_filter = ('entity_type', 'is_available', 'city')
    search_fields = ('entity_name','entity_type','phone_number', 'registration_number', 'city__name',)
    # fields is hidden
    exclude = ['user']
    list_editable = ('is_available',)


    def view_logo(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; border-radius: 8px; object-fit: cover; border: 1px solid #ddd;" />',
                obj.logo.url
            )
        return _("No Logo")

    view_logo.short_description = _("Logo")

    def view_cr_document(self, obj):
        if obj.commercial_register:
            return format_html(
                '<a href="{}" target="_blank" style="color: #2563eb; text-decoration: underline;">{}</a>',
                obj.commercial_register.url, _("View Document"))
        return _("No Document")

    view_cr_document.short_description = _("CR Document")
@admin.register(Industry)
class IndustryAdmin(BaseModelAdmin):
    tailwind_fields = []

    list_display = ( 'name','description',)
    exclude = ['icon']
    search_fields = ('name',)

    def view_icon(self, obj):
        if obj.icon:
            return format_html(
                '<i class="{}"></i>',
                obj.icon
            )
        return ""




