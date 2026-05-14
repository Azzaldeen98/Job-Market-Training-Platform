from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.helpers import get_identities_apps, get_identities_dashboards, get_url_view, app_is_exists, get_app_name
from core.routes import Routes
from .base_models import *
from django.contrib.auth.base_user import BaseUserManager



class Role(BaseRole):

    permissions = models.ManyToManyField(Permission, blank=True, verbose_name=_("Permissions"))
    is_identity = models.BooleanField(default=True)
    requires_approval = models.BooleanField(
        default=False,
        verbose_name = _("Require Approval"),
        help_text=_("Does a member of this role need administrative approval before activating their account?")
    )

    view_in_register = models.BooleanField(default=False, verbose_name=_("Show in Register"))

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        identity_data = extra_fields.get('identity')

        # التحقق من نوع البيانات الواصلة (هل هي كائن أم رقم معرف؟)
        if identity_data:
            if isinstance(identity_data, Role):
                role_obj = identity_data
            else:
                # إذا كان ID، نقوم بجلب الكائن من قاعدة البيانات
                role_obj = Role.objects.filter(id=identity_data).first()

            # الآن نطبق منطق الأتمتة بأمان
            if role_obj and role_obj.requires_approval:
                # extra_fields['is_active'] = False
                extra_fields.setdefault('is_verified', False)
            else:
                extra_fields.setdefault('is_verified', True)

            extra_fields['is_active'] = True

        else:
            # حالة افتراضية إذا لم يتم تمرير هوية (مثل الأدمن)
            extra_fields.setdefault('is_active', True)
            extra_fields.setdefault('is_verified', False)



        if not email:
            raise ValueError(_('The Email must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(BaseCustomUser):

    objects = CustomUserManager()
    identity = models.ForeignKey( Role,
        on_delete=models.PROTECT,
        null=True,blank=True,
        limit_choices_to={'is_identity': True},
        verbose_name="Identity type",
        related_name="identity_users"
    )
    is_verified = models.BooleanField( _("Is Verified"),
     default=False,
     help_text=_("Activated by administrator after log review")
    )

    @property
    def profile(self):
        if not self.identity: return None
        elif self.is_training_entity: return getattr(self, 'training_profile', None)
        elif self.is_student: return getattr(self, 'student_profile', None)
        return None

    @property
    def get_role(self):
        return '' if not self.identity else   self.identity.code

    def has_role(self, role_code):
      return False if not self.identity else  self.identity.code == role_code

    @property
    def role_name(self):
        return 'User' if not self.identity \
            else self.identity.name

    @property
    def is_training_entity(self):
        return self.has_role('training_entity')

    @property
    def is_student(self):
        return self.has_role('student')

    @property
    def is_identity(self):
        return False  if not self.identity \
            else getattr(self.identity, 'is_identity', False)

    @property
    def is_fully_active(self):
        """
        التحقق من التفعيل بناءً على الهوية الواحدة (Identity) والبروفايل:
        """
        # 1. إذا لم يكن للمستخدم هوية أصلاً
        if not self.identity:
            return False

        # 2. إذا كانت الهوية لا تتطلب موافقة (مثل طالب) -> مفعل فوراً
        if not self.identity.requires_approval:
            return True

        # 3. إذا كانت تتطلب موافقة (مثل شركة) -> نتحقق من البروفايل المرتبط
        # نستخدم self.profile الذي يعمل عبر GenericForeignKey
        if self.profile and hasattr(self.profile, 'is_verified'):
            return self.profile.is_verified and self.is_active

        # الافتراضي: غير مفعل حتى يثبت العكس
        return False

    @property
    def is_approved_entity(self):
        return self.is_training_entity and  self.is_verified and self.is_active

    # داخل كلاس CustomUser في models.py
    @property
    def get_app_name(self):
        if self.is_authenticated and self.is_identity:
            role_code = getattr(self.identity, 'code', None)
            if role_code:
                app_name = get_app_name(role_code)
                if app_name:
                    return app_name
                # identities_apps = get_identities_apps()
                # if identities_apps:
                #     return identities_apps[role_code]
        return None

    @property
    def get_dashboard_url(self):

        if self.is_authenticated and self.is_identity:
            role_code = getattr(self.identity, 'code', None)
            if role_code:
                app_name = self.get_app_name
                if app_is_exists(app_name):
                    dashboards = get_identities_dashboards()
                    if dashboards:
                        dashboard_url = dashboards.get(role_code, Routes.HOME)
                        return get_url_view(dashboard_url)

        return Routes.HOME



# --- بروفايلات منفصلة بجداول منفصلة ---
# class Profile(BaseProfile):
#
#     bio = models.TextField(max_length=500, blank=True, verbose_name=_("bio"))
#     pass




#
# class CompanyProfile(BaseProfile):
#     tax_number = models.CharField(max_length=50, verbose_name=_("Tax Number"))
#     company_name = models.CharField(max_length=200, verbose_name=_("Company Name"))
#
#     address = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Address"))
#     city = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("City"))
#     country = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Country"))
#     bio = models.TextField(max_length=500, blank=True, verbose_name=_("Bio"))


# class CustomUser(AbstractUser):
#     email = models.EmailField(_('email address'), unique=True)
#     phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("phone number"))
#
#     profile_picture = models.ImageField(upload_to='users/profiles/%Y/%m/', blank=True, null=True,
#                                         verbose_name=_("profile picture"))
#     bio = models.CharField(max_length=500, blank=True)
#     birth_date = models.DateField(null=True, blank=True, verbose_name=_("birth date"))
#
#     # ربط الدور (ForeignKey) - كما طلبت لمرونة المشاريع الكبيرة
#     # role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users',
#     #                          verbose_name=_("User Role"))
#     # التفضيلات والتتبع
#     is_dark_mode = models.BooleanField(default=False, verbose_name=_("dark mode"))
#     language_preference = models.CharField(max_length=5, choices=[('ar', 'العربية'), ('en', 'English')], default='ar',
#                                            verbose_name=_("preferred language"))
#     bio = models.CharField(max_length=500,  blank=True)
#     last_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_("last login IP"))
#
#     def has_role_perm(self, perm_name):
#         """
#         دالة مساعدة للتحقق مما إذا كان دور المستخدم يملك صلاحية معينة
#         """
#         if self.is_superuser:
#             return True
#         if self.role:
#             return self.role.permissions.filter(codename=perm_name).exists()
#         return False
#
#
#     class Meta:
#         verbose_name = _("user")
#         verbose_name_plural = _("users")
#         ordering = ['-date_joined']
#
#     def __str__(self):
#         return f"{self.username} ({self.email})"

# # --- 3. جداول الملفات التخصصية (Profiles) ---
#
# class StudentProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
#     university = models.CharField(max_length=255, blank=True)
#     cv_file = models.FileField(upload_to='users/cvs/', blank=True)
#     # أضف أي حقول تخص الطالب هنا
#
#
# class CompanyProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='company_profile')
#     company_name = models.CharField(max_length=255, blank=True)
#     is_approved = models.BooleanField(default=False)
#     # أضف أي حقول تخص الشركة هنا
#
#
# # --- 4. محرك الربط التلقائي (Signals) ---
# @receiver(post_save, sender=CustomUser)
# def manage_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role:
#         # الربط يعتمد على "اسم الدور" في جدول الأدوار
#         role_name = instance.role.name.upper()
#         if role_name == "STUDENT":
#             StudentProfile.objects.get_or_create(user=instance)
#         elif role_name == "COMPANY":
#             CompanyProfile.objects.get_or_create(user=instance)

