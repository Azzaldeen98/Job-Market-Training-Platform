from django.utils.translation import gettext_lazy as _

from core.constants import BaseMessages

class TrainingMessages(BaseMessages):
    DELETE_WARNING_OPPORTUNITY = _(
        "Are you sure you want to delete this opportunity? All associated data will be permanently removed.")

