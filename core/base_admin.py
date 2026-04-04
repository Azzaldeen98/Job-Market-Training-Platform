
from django import forms
from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class BaseModelAdmin(admin.ModelAdmin):

    tailwind_fields = []

    base_css = "w-full bg-base text-content border border-stroke-soft px-4 py-2 mt-1 rounded-lg focus:ring-2 transition duration-200 outline-none shadow-sm"

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
                'class': f"{base_css} appearance-none"
            })
        },
        models.ManyToManyField: {
            'widget': forms.SelectMultiple(attrs={
                'class': base_css,
                'style': 'min-height: 120px;'
            })
        },
    }

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)

        # التحقق إذا كان اسم الحقل مرسل ضمن القائمة
        if db_field.name in self.tailwind_fields:
            # كلاسات التنسيق الأساسية (بدون w-full لتجنب مشكلة الأزرار)
            custom_class = "flex-1 bg-base text-content border border-stroke-soft px-4 py-2 mt-1 rounded-lg focus:ring-2 transition duration-200 outline-none shadow-sm"

            # إذا كان الحقل عبارة عن قائمة منسدلة (Enum أو ForeignKey)
            if db_field.choices or isinstance(db_field, models.ForeignKey):
                custom_class += " cursor-pointer appearance-none bg-[url('data:image/svg+xml;...')] bg-no-repeat bg-right"

            # تطبيق الكلاسات على الـ Widget
            field.widget.attrs.update({'class': custom_class})

        return field


    # def changelist_view(self, request, extra_context=None):
    #     # تعطيل الحقن البرمجي مؤقتاً للتأكد من زوال الخطأ
    #     return super().changelist_view(request, extra_context=extra_context)
    def changelist_view(self, request, extra_context=None):
        app_label = self.model._meta.app_label
        model_name = self.model._meta.model_name
        add_url = reverse(f'admin:{app_label}_{model_name}_add')
        btn_text = f"{_('Add')} {self.model._meta.verbose_name}"

        # حقن كود JS يضيف الزر في الـ DOM مباشرة
        # هذا الكود يبحث عن مكان البحث ويضع الزر بجانبه
        script = format_html('''
            <script>
                document.addEventListener("DOMContentLoaded", function() {{
                    if (!document.getElementById("custom-add-btn")) {{
                        var container = document.getElementById("changelist-search") || document.querySelector(".object-tools");
                        var btn = document.createElement("a");
                        btn.id = "custom-add-btn";
                        btn.href = "{}";
                        btn.innerHTML = "{}";

                        btn.style = "background:#9333EA; color:white; padding:8px 16px; border-radius:6px; text-decoration:none; margin: 10px; display:inline-block; font-weight:bold;";
                        container.prepend(btn);
                    }}
                }});
            </script>
        ''', add_url, btn_text)

        self.message_user(request, script, level='INFO')
        return super().changelist_view(request, extra_context=extra_context)

class BaseTabularInline(admin.TabularInline):
    # كلاس أب لتنسيق الجداول التابعة (Inlines)
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)

        # كلاس التنسيق الخاص بك (نفس الموجود في الأب)
        custom_class = "w-full bg-base text-content border border-stroke-soft px-4 py-2 mt-1 rounded-lg shadow-sm focus:ring-2 outline-none"

        # تطبيق التنسيق على حقول النصوص والقوائم المنسدلة
        if isinstance(db_field, (models.CharField, models.ForeignKey)):
            field.widget.attrs.update({'class': custom_class})

        return field


