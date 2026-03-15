
from django.db import models
from django.utils.translation import gettext_lazy as _

class UniversityType(models.TextChoices):
    PUBLIC = 'PUB', _('Governmental')
    PRIVATE = 'PRI', _('Private')
    INTERNATIONAL = 'INT', _('International')
    TECHNICAL = 'TEC', _('Technical')


