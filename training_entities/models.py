from django.db import models
from django.utils.translation import gettext_lazy as _
from academy.models import Skill, Major
from config import settings
from core.base_models import BaseModel
from core.models import City
from core.utils import current_date
from training_entities.enums import EntityType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class TrainingEntityProfile(models.Model):

    user = models.OneToOneField( settings.AUTH_USER_MODEL,on_delete=models.CASCADE,
        related_name='training_profile',verbose_name=_("User Account"))

    city = models.ForeignKey(City, on_delete=models.SET_NULL,
        related_name="training_entities",verbose_name=_("City"),
        null=True,blank=True )

    entity_name = models.CharField(_("Training Entity Name"), max_length=255)
    entity_type = models.CharField(_("Training Entity Type"),
        max_length=10,choices=EntityType.choices,
        default=EntityType.PRIVATE)

    description = models.TextField(_("About the Training Entity"), max_length=512, blank=True)
    phone_number = models.CharField(_("Phone Number"), max_length=15, blank=True,
                                    unique=True, null=True)
    registration_number = models.CharField( _("Registration Number"),
        max_length=50,unique=True,)

    logo = models.ImageField( _("Logo"),upload_to='training_entities/logos/',
        null=True,blank=True,
        help_text=_("Preferably 512x512 pixels") )

    cover_image = models.ImageField( _("Cover Image"),
        upload_to='training_entities/covers/',
        null=True, blank=True,
        help_text=_("A high-quality landscape image is preferred"))

    commercial_register = models.FileField(_("Commercial Register"),
        upload_to='training_entities/commercial_registers/',
        null=True, blank=True,
        help_text=_("Upload a copy of your CR or Government ID (PDF)")
    )

    website = models.URLField(_("Website"), unique=True, blank=True, null=True)

    is_available = models.BooleanField(default=False,
        verbose_name=_("Approved State"),
        help_text=_("Determines whether the training provider is accredited to operate.")
    )

    @property
    def is_profile_complete(self):
        required_fields = [self.commercial_register, self.registration_number, self.entity_name, self.entity_type]
        return all(required_fields)


    class Meta:
        verbose_name = _("Training Entity Profile")
        verbose_name_plural = _("Training Entity Profiles")


    @property
    def check_available(self):
        return  self.is_available and self.user.is_active

    @property
    def get_logo_url(self):
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url
        return ''  # مسار صورة افتراضية





    def __str__(self):
        return self.entity_name

    # extra_data = models.JSONField(default=dict, blank=True, verbose_name=_("Extra Data"))

"""
User Role: Admin
Access Permissions: Only Admin are permitted to create, update, or delete data.
Training Provider: Read-only permissions; specify the training opportunity area.
"""
class Industry(models.Model):
    name = models.CharField(
        _("Industry Name"),
        max_length=100,
        unique=True,
        # help_text=_("مثلاً: التقنية، الصحة، الهندسة، البنوك")
    )

    icon = models.CharField(
        _("Icon Class"),
        max_length=50,
        blank=True,
        null=True,
    )

    description = models.TextField(_("Description"), blank=True, null=True)

    class Meta:
        verbose_name = _("Industry")
        verbose_name_plural = _("Industries")
        ordering = ['name']

    def __str__(self):
        return self.name

"""
User Role: Trainer
Access Permissions: Only users with the "Trainer" role are permitted to create, update, or delete data.
Students: Read-only permission to view opportunities.
"""
class TrainingOpportunity(BaseModel):

    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('pending', _('Pending Review')),
        ('open', _('Open')),
        ('closed', _('Closed')),
    ]

    # ربط الفرصة بجهة التدريب
    provider = models.ForeignKey(
        TrainingEntityProfile,
        on_delete=models.CASCADE,
        related_name='opportunities',
        verbose_name=_("Training Provider")
    )

    title = models.CharField(_("Opportunity Title"), max_length=255)
    description = models.TextField(_("Description"))

    # تصنيف المجال (مثل: تقنية، هندسة، إدارة)
    field = models.ForeignKey(
        Industry,
        on_delete=models.SET_NULL,
        null=True,
        related_name="opportunities",
        verbose_name=_("Field/Industry")
    )

    # تفاصيل الموقع الجغرافي
    city = models.ForeignKey(
        City,  # افترضت وجود موديل City
        on_delete=models.SET_NULL,
        related_name="training_opportunities",
        verbose_name=_("City"),
        null=True,
        blank=True,
    )

    # التواريخ
    start_date = models.DateField(_("Start Date"), null=True,blank=True,)
    end_date = models.DateField(_("End Date"), null=True,blank=True,)
    deadline = models.DateField(_("Application Deadline"), null=True,blank=True,)

    # السعة والمتطلبات الأكاديمية
    capacity = models.PositiveIntegerField(_("Capacity"), validators=[MinValueValidator(1)], null=True,blank=True,)

    # majors = models.ManyToManyField(
    #     Major,
    #     related_name='opportunities',
    #     verbose_name=_("Target Majors"),
    #     help_text=_("Choose the university majors required for this opportunity")
    # )
    # models.py
    major = models.ForeignKey(
        Major,
        on_delete=models.CASCADE,  # أو models.SET_NULL مع null=True إذا كنت لا تريد حذف الفرصة عند حذف التخصص
        related_name='opportunities',
        verbose_name=_("Target Major"),
        help_text=_("Choose the university major required for this opportunity")
    )

    # المهارات
    required_skills = models.ManyToManyField(
        Skill,
        related_name='opportunities',
        verbose_name=_("Required Skills"),
    )

    other_skills_notes = models.TextField(_("Other Skills/Tools Notes"), blank=True, null=True)

    # دمجنا متطلبات الوصف في حقل واحد شامل
    additional_requirements = models.TextField(
        _("Additional Requirements"),
        blank=True,
        null=True,
        help_text=_("Describe any other conditions like GPA, gender, or specific tools.")
    )
    # المقياس
    gpa_scale = models.PositiveSmallIntegerField(
        _("GPA Scale"),
        choices=[
            (4, '4.0'),
            (5, '5.0'),
            (100, '100%')
        ],
        default=0,
        help_text=_("Choose the approved grading system (4, 5, 100%) (optional)")
    )

    # المعدل الأكاديمي
    min_gpa = models.DecimalField(
        _("Minimum GPA"),
        max_digits=4,  #  يسمح بالقيم من 0.00 الى 99.99
        decimal_places=2,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(100.0)
        ],
        help_text=_("Enter the minimum required score based on the selected scale (optional)")
    )


    # المزايا
    benefits = models.TextField(
        _("Benefits"),
        blank=True,
        null=True,
        help_text=_("Enter the benefits offered to the trainee student.")
    )

    # الحالة والتوقيت
    status = models.CharField(_("Status"), max_length=20,  choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Training Opportunity")
        verbose_name_plural = _("Training Opportunities")
        ordering = ['-created_at']

    def __str__(self):
        # تم تعديل الوصول للاسم ليكون أكثر أماناً باستخدام getattr
        provider_name = getattr(self.provider, 'name', 'Unknown')
        return f"{self.title} - {provider_name}"

    def get_percentage(self):
        """تحويل أي معدل إلى نسبة مئوية من 100"""
        if self.gpa_scale == 0: return 0
        return (self.gpa / self.gpa_scale) * 100



    def clean(self):
        super().clean()
        if self.min_gpa and self.gpa_scale:
            # إذا كان المقياس 4 أو 5 والمعدل المدخل أكبر منهما
            if self.gpa_scale in [4, 5] and self.min_gpa > self.gpa_scale:
                raise ValidationError({
                    'min_gpa': f"المعدل لا يمكن أن يكون أكبر من {self.gpa_scale} بناءً على المقياس المختار."
                })


    def get_app_name(self):
        return 'training_entities'

    def get_delete_url(self):
        # يجب إضافة الأقواس () هنا لاستدعاء الدالة والحصول على النص 'training_entities'
        return self.get_url(f'{self.get_app_name()}:opportunity_delete', [self.id])

    def get_edit_url(self):
        return self.get_url(f'{self.get_app_name()}:opportunity_edit', [self.id])

    def get_detail_url(self):
        # print(f"Detail:9999999999999")
        url=self.get_url(f'{self.get_app_name()}:opportunity_detail', [self.id])
        print(f"Detail:{url}")
        return url

    def get_check_match_url(self):
        return self.get_url(f'{self.get_app_name()}:check_match', [self.id])

    def is_expired(self):
        """تحقق مما إذا كان تاريخ اليوم قد تجاوز تاريخ الانتهاء"""
        return current_date() > self.end_date

    @property
    def days_left(self):
        """حساب عدد الأيام المتبقية (إذا لم تنتهِ بعد)"""
        today = current_date()
        if today <= self.end_date:
            delta = self.end_date - today
            return delta.days
        return 0

