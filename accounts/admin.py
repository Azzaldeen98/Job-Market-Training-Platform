
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib import admin
from unfold.admin import ModelAdmin
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from allauth.socialaccount.admin import (
    SocialAppAdmin as OldSocialAppAdmin,
    SocialAccountAdmin as OldSocialAccountAdmin,
    SocialTokenAdmin as OldSocialTokenAdmin,
)
from django.utils.translation import gettext_lazy as _





class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # 1. تخصيص الحقول في صفحة التعديل
    fieldsets = UserAdmin.fieldsets + (
        (_('Additional Settings'), {
            'fields': ('is_dark_mode', 'language_preference', 'phone_number', 'picture', 'is_verified')
        }),
    )

    # 2. تخصيص الأعمدة في القائمة الرئيسية
    list_display = ['username', 'email', 'role_name','is_verified', 'is_active', 'is_dark_mode']

    # 3. السماح بتغيير حالة التوثيق مباشرة من القائمة دون الدخول لصفحة المستخدم
    list_editable = ['is_verified', 'is_active']

    # 4. إضافة فلاتر جانبية لتسهيل الوصول للمستخدمين غير الموثقين
    list_filter = UserAdmin.list_filter + ('is_verified', 'is_dark_mode'    )

    # 5. إضافة عمليات جماعية (Bulk Actions)
    actions = ['approve_users', 'deactivate_users']

    def role_name(self, obj):
        return obj.role_name

    @admin.action(description=_("Approve selected users (Set as Verified)"))
    def approve_users(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, _(f"Successfully verified {updated} users."))

    @admin.action(description=_("Deactivate selected users"))
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, _(f"Successfully deactivated {updated} users."))

    role_name.short_description = _('Role')
admin.site.register(CustomUser, CustomUserAdmin)

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     # عرض الحقول الجديدة في صفحة التعديل
#     fieldsets = UserAdmin.fieldsets + (
#         (_('Additional Settings'), {'fields': ('is_dark_mode', 'language_preference', 'phone_number', 'picture')}),
#     )
#     # عرض الحقول في قائمة المستخدمين الرئيسية
#     list_display = ['username', 'email','is_verified','is_dark_mode']
#
# admin.site.register(CustomUser, CustomUserAdmin)

# إلغاء التسجيل القديم لتجنب التكرار
admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)

# إعادة التسجيل باستخدام تنسيق Unfold
@admin.register(SocialApp)
class SocialAppAdmin(OldSocialAppAdmin, ModelAdmin):
    pass

@admin.register(SocialAccount)
class SocialAccountAdmin(OldSocialAccountAdmin, ModelAdmin):
    pass

@admin.register(SocialToken)
class SocialTokenAdmin(OldSocialTokenAdmin, ModelAdmin):
    pass