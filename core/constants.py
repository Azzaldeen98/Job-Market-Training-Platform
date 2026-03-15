from django.utils.translation import gettext_lazy as _
class BaseMessages:
    # رسائل عامة تستخدم في كل التطبيقات
    REQUIRED_FIELD = _("This field is required.")
    INVALID_PDF_EXTENSION = _("Only PDF files are allowed.")
    DELETE_WARNING = _("Are you sure? All associated data will be permanently removed.")
    SAVE_SUCCESS = _("Data has been saved successfully.")

class FormErrorMessages(BaseMessages):
    PHONE_START = _("The mobile number must start with 05.")
    PHONE_LEN = _("Must be 10 digits.")
    GRADUATION_YEAR = _("Graduation year cannot be in the far future.")
    GPA_OUT_RANGE = _("GPA must be between 0 and 5.00.")
    # DELETE_WARNING = _("Are you sure you want to delete this item? This action cannot be undone")
