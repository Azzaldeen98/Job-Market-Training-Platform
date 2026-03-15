from django.db import models
from django.utils.translation import gettext_lazy as _

from academy.enums import UniversityType
from core.models import City


# Create your models here.

class University(models.Model):

    name = models.CharField(_("University Name"), max_length=255, blank=True)
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="universities",
        verbose_name=_("City")
    )

    type = models.CharField(
        _("University Type"),
        max_length=3,
        choices=UniversityType.choices,
        default=UniversityType.PUBLIC,
    )
    # latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    # longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    def __str__(self):
        return f"{self.name}"

class College(models.Model):
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name="colleges",
        verbose_name=_("University")
    )
    name = models.CharField(_("College Name"), max_length=255)
    def __str__(self):
        return f"{self.name}"

class Major(models.Model):

    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        related_name="majors",
        verbose_name=_("College")
    )
    name = models.CharField(_("name"), max_length=255, blank=False)
    description = models.CharField(_("description"), max_length=255, blank=True)

    def __str__(self):
        return f"{self.name}"


class SkillCategory(models.Model):
    name = models.CharField(_("Category Name"), max_length=150, unique=True)
    icon_name = models.CharField(
        _("Icon Name"),
        max_length=50,
        help_text=_("Lucide or FontAwesome icon name (e.g., 'terminal')"),
        default='tag'
    )

    def __str__(self):
        return self.name


class Skill(models.Model):

    name = models.CharField(_("Skill Name"), max_length=150, unique=True)
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        null=True,
        related_name="skills"
    )

    def __str__(self):
        return self.name