from django.db import models
from django.utils.translation import gettext_lazy as _

# from core.enums import UniversityType


# Create your models here.

class Country(models.Model):
    name = models.CharField(_("name"), max_length=255, blank=False)
    code = models.CharField(_("code"), max_length=10, unique=True, blank=False)
    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(_("name"), max_length=255, blank=False)
    code = models.CharField(_("code"), max_length=10, unique=True, blank=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="regions")
    def __str__(self):
        return f"{self.name}"


class City(models.Model):
    name = models.CharField(_("name"), max_length=255, blank=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="cities")
    def __str__(self):
        return f"{self.name}"








