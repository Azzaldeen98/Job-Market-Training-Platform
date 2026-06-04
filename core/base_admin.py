
from django import forms
from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

class GlobalAdminStyle(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/admin_styles.css')
        }

class BaseModelAdmin(admin.ModelAdmin):

    tailwind_fields = []
    base_css = "d-flex w-full bg-base text-content border border-stroke-soft px-4 py-2 mt-1 rounded-lg focus:ring-2 transition duration-200 outline-none shadow-sm"
    formfield_overrides = {

        models.CharField: {
            'widget': forms.TextInput(attrs={
                'class': base_css
            })
        },
        models.TextField: {
            'widget': forms.Textarea(attrs={
                'class': base_css,
                 'rows': 4
            })
        },
        models.ForeignKey: {
            'widget': forms.Select(attrs={
                'class': f"{base_css} appearance-none ",
                'style': 'min-width: 200px; display: inline-block;'
            })
        },
        models.ManyToManyField: {
            'widget': forms.SelectMultiple(attrs={
                'class': base_css,
                'style': 'min-height: 120px;'
            })
        },
    }
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        from django.utils.safestring import mark_safe
        custom_style = mark_safe("""
            <style>
                 
                .related-widget-wrapper {
                    display: flex !important;
                    align-items: center !important;
                    gap: 10px !important;
                    width: 100%;
                }
                .related-widget-wrapper-link {
                    display: inline-flex !important;
                    margin: 0 !important;
                }
                .related-widget-wrapper img {
                    width: 16px !important;
                    height: 16px !important;
                }
            </style>
        """)
        context.update({'extra_style': custom_style})
        return super().render_change_form(request, context, add, change, form_url, obj)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in self.tailwind_fields:
            custom_class = "flex-1 bg-base text-content border border-stroke-soft px-4 py-2 mt-1 rounded-lg focus:ring-2 transition duration-200 outline-none shadow-sm"
            if db_field.choices or isinstance(db_field, models.ForeignKey):
                custom_class += " cursor-pointer appearance-none bg-[url('data:image/svg+xml;...')] bg-no-repeat bg-right"
            field.widget.attrs.update({'class': custom_class})

        return field

    def changelist_view(self, request, extra_context=None):

        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        add_url = reverse(f'admin:{app_label}_{model_name}_add')
        btn_text = f"{_('Add')} {self.model._meta.verbose_name}"
        script = format_html('''
            <script>
                document.addEventListener("DOMContentLoaded", function() {{
                    if (!document.getElementById("custom-add-btn")) {{
                        var container = document.getElementById("changelist-search") || document.querySelector(".object-tools");
                        var btn = document.createElement("a");
                        btn.id = "custom-add-btn";
                        btn.href = "{}";
                        btn.innerHTML = "{}";
                    
                        btn.style = "background:#096; color:white; padding:8px 16px; border-radius:6px; text-decoration:none; margin: 10px; display:inline-block; font-weight:bold;";
                        container.prepend(btn);
                    }}
                }});
            </script>
        ''', add_url, btn_text)
        # #9333ea
        self.message_user(request, script, level='INFO')
        return super().changelist_view(request, extra_context=extra_context)

class BaseTabularInline(admin.TabularInline):

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        custom_class = "w-full bg-base text-content border border-stroke-soft px-4 py-2 mt-1 rounded-lg shadow-sm focus:ring-2 outline-none"
        if isinstance(db_field, (models.CharField, models.ForeignKey)):
            field.widget.attrs.update({'class': custom_class})

        return field


