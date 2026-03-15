
import os
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible




@deconstructible
class FileValidator:
    """
    Validator to check file size (in MB) and allowed extensions.
    """

    def __init__(self, max_size_mb=None, allowed_extensions=None, error_messages=None):
        # تحويل الميجا بايت إلى بايت (1 MB = 1024 * 1024 Bytes)
        self.max_size = max_size_mb * 1024 * 1024 if max_size_mb else None
        self.max_size_mb = max_size_mb # نحتفظ بالقيمة الأصلية لعرضها في رسالة الخطأ
        self.allowed_extensions = [ext.lower().strip('.') for ext in allowed_extensions] if allowed_extensions else None

        # رسائل افتراضية قابلة للترجمة
        self.default_messages = {
            'max_size': _("File too large. Maximum size is {size} MB.").format(size=max_size_mb),
            'extension': _("Unsupported file extension. Allowed: {exts}.").format(
                exts=', '.join(self.allowed_extensions or [])
            )
        }
        self.error_messages = {**self.default_messages, **(error_messages or {})}

    def __call__(self, file):
        if not file:
            return

        # 1. التحقق من الحجم (مقارنة البايت بالبايت)
        if self.max_size and file.size > self.max_size:
            message = self.error_messages.get('max_size')
            raise ValidationError(message, code='file_too_large')

        # 2. التحقق من الامتداد
        extension = os.path.splitext(file.name)[1][1:].lower()
        if self.allowed_extensions and extension not in self.allowed_extensions:
            message = self.error_messages.get('extension')
            raise ValidationError(message, code='invalid_extension')

@deconstructible
class PhoneValidator:
    """
    مصدق عام لأرقام الهاتف يدعم:
    1. التحقق من البداية (Prefix).
    2. التحقق من الطول (Length).
    3. رسائل افتراضية بالإنجليزية مع إمكانية التخصيص.
    """

    def __init__(self, prefix='05', length=10, error_messages=None):
        self.prefix = prefix
        self.length = length

        # الرسائل الافتراضية بالإنجليزية
        self.default_messages = {
            'invalid_start': f"Phone number must start with {self.prefix}.",
            'invalid_length': f"Phone number must be exactly {self.length} digits long.",
            'not_digit': "Phone number must contain only digits."
        }

        # دمج الرسائل المخصصة مع الافتراضية
        self.error_messages = {**self.default_messages, **(error_messages or {})}

    def __call__(self, value):
        if not value:
            return

        # 1. التحقق أن القيمة أرقام فقط (اختياري حسب نوع الحقل)
        if not value.isdigit():
            raise ValidationError(self.error_messages.get('not_digit'), code='not_digit')

        # 2. التحقق من البداية
        if self.prefix and not value.startswith(self.prefix):
            raise ValidationError(self.error_messages.get('invalid_start'), code='invalid_start')

        # 3. التحقق من الطول
        if self.length and len(value) != self.length:
            raise ValidationError(self.error_messages.get('invalid_length'), code='invalid_length')




