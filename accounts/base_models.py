from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class BaseRole(models.Model):
    name = models.CharField(max_length=50,unique=True, verbose_name=_("Role Name"))
    code = models.SlugField(max_length=20, unique=True, verbose_name=_("Role Key/Code"))
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_("A brief description of this role's permissions")
    )

    class Meta:
        abstract = True
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

    def __str__(self):
        return f"{self.name} ({self.code})"


class BaseCustomUser(AbstractUser):

    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("phone number"))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_("birth date"))
    # هذا السطر يخبر Django باستخدام البريد للدخول
    USERNAME_FIELD = 'email'

    # الحقول المطلوبة عند إنشاء Superuser (بالإضافة للبريد وكلمة المرور)
    REQUIRED_FIELDS = ['username']
    is_dark_mode = models.BooleanField(default=False, verbose_name=_("dark mode"))
    language_preference = models.CharField(
        max_length=5,
        choices=[('ar', 'العربية'), ('en', 'English')],
        default='ar',
        verbose_name=_("preferred language")
    )
    last_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_("last login IP"))
    # --- حقول الربط الديناميكي (The Magic Logic) ---
    # تخزين نوع جدول البروفايل (طالب، شركة، إلخ)
    profile_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_profiles")
    # تخزين رقم المعرف داخل ذلك الجدول
    profile_id = models.PositiveIntegerField(null=True, blank=True)
    # الحقل الذي ستستخدمه في الكود للوصول لأي بروفايل
    profile = GenericForeignKey('profile_type', 'profile_id')


    class Meta:
        abstract = True
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ['-date_joined']

    # def has_role(self, role_code):
    #     return self.roles.filter(code=role_code).exists()
    #
    # def is_fully_active(self):
    #     """
    #     التحقق من التفعيل:
    #     1. إذا لم يكن هناك أدوار تتطلب موافقة -> True
    #     2. إذا وجد دور يتطلب موافقة -> نتحقق من حقل is_verified داخل البروفايل المرتبط
    #     """
    #     roles_needing_approval = self.roles.filter(requires_approval=True)
    #     if not roles_needing_approval.exists():
    #         return True
    #
    #     # الوصول للبروفايل عبر GenericForeignKey
    #     if self.profile and hasattr(self.profile, 'is_verified'):
    #         return self.profile.is_verified
    #
    #     return False


class BaseProfile(models.Model):
    # حقول مشتركة لكل أنواع البروفايلات
    picture = models.ImageField(
        upload_to='users/profiles/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_("Picture")
    )
    is_verified = models.BooleanField(default=False, verbose_name=_("Is Verified Account"))
    extra_data = models.JSONField(default=dict, blank=True, verbose_name=_("Extra Data"))

    class Meta:
        abstract = True