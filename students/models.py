from django.db import models
from django.utils.translation import gettext_lazy as _

from academy.models import Major, Skill
from config import settings
from core.base_models import BaseProfile, BaseModel



# Create your models here.
class StudentProfile(BaseModel):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name=_("User Account")
    )

    major = models.ForeignKey(
        Major,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
        verbose_name=_("Major")
    )

    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    phone_number = models.CharField(max_length=15, blank=True, unique=True, null=True, verbose_name=_("phone number"))
    picture = models.ImageField(
        upload_to='students/profiles/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_("Picture")
    )
    # birth_date = models.DateField(null=True, blank=True, verbose_name=_("birth date"))
    graduation_year = models.PositiveIntegerField( _("Graduation Year"),  null=True, blank=True )
    # المعدل التراكمي (GPA)
    gpa = models.DecimalField( _("GPA"), max_digits=4,decimal_places=2, null=True, blank=True)

    # السيرة الذاتية (PDF)
    cv_file = models.FileField(
        _("CV File"),
        upload_to='students/cvs/',
        null=True,
        blank=True)

    is_available = models.BooleanField(default=True,
        verbose_name=_("Available for Training"),
        help_text=_("Designates whether this student is currently looking for an internship.")
    )

    skills = models.ManyToManyField(Skill, related_name="students", blank=True)

    #extra_data = models.JSONField(default=dict, blank=True, verbose_name=_("Extra Data"))

    @property
    def get_full_name(self):
        full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return  full_name

    @property
    def get_app_name(self):
        return  'students'
    def get_opportunities_url(self):
        self.get_url(f'{self.get_app_name}:opportunities', [self.id])

    @property
    # داخل كلاس StudentProfile في models.py
    def card_data(self):
        """تجهيز البيانات بشكل عام للـ core مع حماية كاملة"""

        # حماية الاسم (في حال عدم وجود الاسم الأول أو الأخير)
        full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()

        # حماية الوصول المتسلسل للجامعة
        # نستخدم try/except أو التحقق المتداخل لضمان عدم توقف الكود إذا كان التخصص غير محدد
        university_name = "-"
        location = "-"
        if self.major and self.major.college and self.major.college.university:
            university_name = self.major.college.university.name
            location = self.major.college.university.city.name

        return {
            'title': full_name or self.user.username,
            'image_url': self.picture.url if self.picture else None,  # صورة حقيقية
            'image_icon': 'user',  # أيقونة احتياطية
            'badge': f"ID: #{self.id}",
            'academic_info': [
                {'label': 'University', 'value': university_name},
                {'label': 'College', 'value': self.major.college.name if self.major and self.major.college else "-"},
                {'label': 'Major', 'value': self.major.name if self.major else "-"},
            ],
            'location': {'label': 'City', 'value': location or ''},
            'stats': {'label': 'GPA', 'value': self.gpa or "0.00"},
            'status': [
                {'label': 'Active', 'value': self.user.is_active },
                {'label': 'Available', 'value': self.is_available }
            ],
            'skills': [skill.name for skill in self.skills.all()],  # نمرر الأسماء كنصوص
            'action_url': self.cv_file.url if self.cv_file else None
        }




