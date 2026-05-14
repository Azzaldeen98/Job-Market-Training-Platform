from django.contrib import admin

from academy.models import University, College, Major, SkillCategory, Skill
from core.admin import BaseModelAdmin, BaseTabularInline


class CollegeInline(BaseTabularInline):
    model = College
    extra = 1
    fields = ('name',)

class MajorInline(BaseTabularInline):
    model = Major
    extra = 1
    fields = ('name','description',)

# Register your models here.
@admin.register(University)
class UniversityAdmin(BaseModelAdmin):
    tailwind_fields=['type']

    list_display = ('name','city','type',)
    search_fields = ('name',)
    inlines = [CollegeInline] #

@admin.register(College)
class CollegeAdmin(BaseModelAdmin):
    list_display = ('name','university',)
    search_fields = ('name',)
    list_filter = ('university',)
    inlines = [MajorInline] #


@admin.register(Major)
class MajorAdmin(BaseModelAdmin):
    list_display = ('name','description','college','college__university')
    list_filter = ('college__university', 'college',)
    search_fields = ('name',)

class SkillInline(BaseTabularInline):
    model = Skill
    extra = 1
    fields = ('name',)


@admin.register(SkillCategory)
class SkillCategoryAdmin(BaseModelAdmin):
    list_display = ('name','icon_name')
    search_fields = ('name',)
    inlines = [SkillInline]  #


@admin.register(Skill)
class SkillAdmin(BaseModelAdmin):
    list_display = ('name','category',)
    search_fields = ('name',)
    list_filter = ('category',)



# class AcademyBaseModelAdmin(admin.ModelAdmin):
#     tailwind_fields = []
#     formfield_overrides = {
#         models.CharField: {
#             'widget': forms.TextInput(attrs={
#                 'class': "w-full bg-base text-content border border-stroke-soft px-4 py-2 mt-1 rounded-lg focus:ring-2 transition duration-200 outline-none w-full shadow-sm",
#                 # 'style': 'max-width: 400px;'  # لتحديد العرض
#             })
#         },
#         models.ForeignKey: {
#             'widget': forms.Select(attrs={
#                 'class': "w-full bg-base text-content border border-stroke-soft px-4 py-2 mt-1 rounded-lg focus:ring-2 transition duration-200 outline-none shadow-sm appearance-none",
#                 # أضفنا appearance-none لإلغاء سهم المتصفح الافتراضي إذا كنت تريد تخصيصه
#             })
#         },
#         # models.CharField: {
#         #     'widget': forms.Select(attrs={
#         #         'class': "w-full bg-base text-content border border-stroke-soft px-4 py-2 mt-1 rounded-lg focus:ring-2 transition duration-200 outline-none shadow-sm appearance-none",
#         #     })
#         # },
#     }
#
#     def formfield_for_dbfield(self, db_field, request, **kwargs):
#         field = super().formfield_for_dbfield(db_field, request, **kwargs)
#
#         # التحقق إذا كان اسم الحقل مرسل ضمن القائمة
#         if db_field.name in self.tailwind_fields:
#             # كلاسات التنسيق الأساسية (بدون w-full لتجنب مشكلة الأزرار)
#             custom_class = "flex-1 bg-base text-content border border-stroke-soft px-4 py-2 mt-1 rounded-lg focus:ring-2 transition duration-200 outline-none shadow-sm"
#
#             # إذا كان الحقل عبارة عن قائمة منسدلة (Enum أو ForeignKey)
#             if db_field.choices or isinstance(db_field, models.ForeignKey):
#                 custom_class += " cursor-pointer appearance-none bg-[url('data:image/svg+xml;...')] bg-no-repeat bg-right"
#
#             # تطبيق الكلاسات على الـ Widget
#             field.widget.attrs.update({'class': custom_class})
#
#         return field



