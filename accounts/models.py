from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from .base_models import *
from django.contrib.auth.base_user import BaseUserManager

# class BaseRole(models.Model):
#     # 1. جدول الأدوار المستقل
#     # --- 1. جدول الأدوار مع مفاتيح فريدة ---
#     name = models.CharField(max_length=50, verbose_name=_("Role Name"))
#     # "المفتاح" الذي نستخدمه في الكود (مثلاً: student, company, admin)
#     code = models.SlugField(max_length=20, unique=True, verbose_name=_("Role Key/Code"))
#     permissions = models.ManyToManyField(Permission, blank=True, verbose_name=_("Permissions"))
#     # description = models.TextField(blank=True, verbose_name=_("Description"))
#     requires_approval = models.BooleanField(
#         default=False,
#         help_text=_("هل يحتاج المنتسب لهذا الدور لموافقة الإدارة قبل تفعيل حسابه؟"))
#
#     class Meta:
#         abstract = True
#         verbose_name = _("Role")
#         verbose_name_plural = _("Roles")
#
#     def __str__(self):
#         return f"{self.name} ({self.code})"
#
# class BaseCustomUser(AbstractUser):
#
#         """
#         نموذج مستخدم مخصص يدعم الحقول العامة الأكثر استخداماً
#         في المشاريع الاحترافية.
#         """
#
#         # def validate_age(value):
#         #     if len(value) < 20 :
#         #         raise ValidationError('يجب أن لا تقل عدد الحروف عن 20 حرف .')
#
#         # حقول البيانات الشخصية
#         email = models.EmailField(_('email address'), unique=True)
#         phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("phone number"))
#         picture = models.ImageField(
#             upload_to='users/profiles/%Y/%m/',
#             blank=True,
#             null=True,
#             verbose_name=_("profile picture")  # تم تعديل المسمى ليتناسب مع الملفات
#         )
#         # bio = models.TextField(max_length=500, blank=True, verbose_name=_("bio"))
#         # تصحيح: إضافة مسمى لحقل تاريخ الميلاد
#         birth_date = models.DateField(null=True, blank=True, verbose_name=_("birth date"))
#
#         # حقول التفضيلات
#         is_dark_mode = models.BooleanField(default=False, verbose_name=_("dark mode"))
#         language_preference = models.CharField(
#             max_length=5,
#             choices=[('ar', 'العربية'), ('en', 'English')],
#             default='ar',
#             verbose_name=_("preferred language")
#         )
#
#
#         # حقول التتبع
#         # تعديل: المسمى الأنسب هو "Last IP" وليس "New IP" لبيانات التتبع
#         last_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_("last login IP"))
#
#         class Meta:
#             abstract = True
#             verbose_name = _("user")
#             verbose_name_plural = _("users")
#             ordering = ['-date_joined']
#
#         def __str__(self):
#             return f"{self.username} ({self.email})"
#
#         # دالة احترافية للتحقق من امتلاك دور معين
#         def has_role(self, role_code):
#             return self.roles.filter(code=role_code).exists()
#
#         def is_fully_active(self):
#             """
#             دالة عامة جداً: تتحقق من صلاحية المستخدم بناءً على أدواره.
#             تم نقلها هنا لتكون جزءاً من هوية المستخدم الأساسية.
#             """
#             # 1. جلب الأدوار التي تتطلب موافقة
#             roles_needing_approval = self.roles.filter(requires_approval=True)
#
#             # 2. إذا لم يكن هناك أدوار تتطلب موافقة، فهو نشط تلقائياً
#             if not roles_needing_approval.exists():
#                 return True
#
#             # 3. إذا كان هناك دور يتطلب موافقة، نذهب للتحقق من البروفايل
#             # نستخدم hasattr للتأكد من وجود بروفايل وتجنب الأخطاء
#             if hasattr(self, 'profile'):
#                 return self.profile.is_verified
#
#             return False
#
# class BaseProfile(models.Model):
#     # نستخدم settings.AUTH_USER_MODEL ليكون القالب متوافقاً مع أي مشروع
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='profile',  # اسم عام يسهل الوصول إليه
#         verbose_name=_("User")
#     )
#
#     # حقول الموقع (أساسية في معظم الأنظمة)
#     address = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Address"))
#     city = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("City"))
#     country = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Country"))
#
#     # الوصف
#     bio = models.TextField(max_length=500, blank=True, verbose_name=_("Bio"))
#
#     # التوثيق
#     is_verified = models.BooleanField(default=False, verbose_name=_("Is Verified Account"))
#
#     # الحقل الجوكر (مهم جداً للقالب الأساسي)
#     extra_data = models.JSONField(default=dict, blank=True, verbose_name=_("Extra Data"))
#
#     class Meta:
#         abstract = True  # هذه أهم إضافة لجعله قالب (Base)
#
#     # def is_fully_active(self):
#     #     # نتحقق مما إذا كان أي دور من أدوار المستخدم يتطلب موافقة الإدارة
#     #     roles_needing_approval = self.user.roles.filter(requires_approval=True)
#     #
#     #     if roles_needing_approval.exists():
#     #         # هنا نستخدم is_verified كشرط للموافقة
#     #         # (أو يمكنك إضافة حقل status=['pending', 'approved'] إذا أردت دقة أكثر)
#     #         return self.is_verified
#     #
#     #     # إذا لم تكن هناك أدوار تتطلب موافقة، فالحساب نشط تلقائياً
#     #     return True


# 1. الموديل الحقيقي للأدوار

# class IdentityRole(BaseRole):
#     # حقل لتحديد هل تظهر هذه الهوية في صفحة التسجيل للعامة أم للمدير فقط
#     # view_in_register = models.BooleanField(default=False, verbose_name=_("Show in Register"))
#     view_in_register = models.BooleanField(
#         default=False,
#         verbose_name=_("Show in Register"),
#         help_text=_("If enabled, this role will appear as an option for new users when creating an account")
#     )
#
#     requires_approval = models.BooleanField(
#         default=False,
#         help_text=_("Does a member of this role need administrative approval before activating their account?")
#     )
#     class Meta:
#         verbose_name = _("Primary Identity")
#         verbose_name_plural = _("Primary Identities")
#


# class SubRole(BaseRole):
#
#     # Link to the parent identity (1-to-many relationship)
#     # Example: The subrole "Head of Department" is only available to the identity "Teacher"
#
#     parent_identity = models.ForeignKey(
#         IdentityRole,
#         on_delete=models.CASCADE,
#         related_name="available_sub_roles",
#         verbose_name=_("Belongs to Identity")
#     )
#
#     class Meta:
#         verbose_name = _("Sub-Role / Permission Package")
#         verbose_name_plural = _("Sub-Roles / Permission Packages")


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
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(BaseCustomUser):

    objects = CustomUserManager()
    # roles = models.ManyToManyField(Role, blank=True, related_name='users', verbose_name=_("Roles"))
    identity = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        limit_choices_to={'is_identity': True},  # لا يظهر هنا إلا الهويات
        verbose_name="Identity type",
        related_name="identity_users"
    )

    def has_role(self, role_code):
        """
        التحقق من دور المستخدم الحالي (0% أخطاء - تعامل مباشر مع ForeignKey)
        """
        if not self.identity:
            return False
        return self.identity.code == role_code

    def is_company(self):
        return self.has_role('company')

    @property
    def is_student(self):
        return self.has_role('student')

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
            return self.profile.is_verified

        # الافتراضي: غير مفعل حتى يثبت العكس
        return False

# --- بروفايلات منفصلة بجداول منفصلة ---
class Profile(BaseProfile):
    bio = models.TextField(max_length=500, blank=True, verbose_name=_("bio"))
    pass

# class StudentProfile(BaseProfile):
#     university = models.CharField(max_length=100, verbose_name=_("University"))
#     major = models.CharField(max_length=100, verbose_name=_("Major"))
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

