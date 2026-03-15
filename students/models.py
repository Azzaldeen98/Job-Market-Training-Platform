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
    def get_app_name(self):
        return  'students'
    def get_opportunities_url(self):
        self.get_url(f'{self.get_app_name}:opportunities', [self.id])