from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class EntityType(models.TextChoices):

    PRIVATE = 'PRIVATE', _('Private Company/Sector')
    GOVERNMENT = 'GOV', _('Government Entity')
    NON_PROFIT = 'NGO', _('Non-Profit Organization')
    RESEARCH = 'RESEARCH', _('Research Center/Academic Center')