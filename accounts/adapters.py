from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


class MyAccountAdapter(DefaultAccountAdapter):

    def confirm_login_allowed(self, user):
        """
        هذه الدالة يتم استدعاؤها من قبل allauth قبل إتمام عملية تسجيل الدخول.
        """
        # 1. فحص النشاط (is_active)
        if not user.is_active:
            raise ValidationError(
                _("This account is inactive."),
                code='inactive'
            )

        # 2. فحص التحقق (is_verified)
        # نفترض أنك أضفت حقل is_verified لموديل المستخدم
        if hasattr(user, 'is_verified') and not user.is_verified:
            raise ValidationError(
                _("Your account is not verified. Please verify your email first."),
                code='not_verified'
            )

        # استكمال التحقق الطبيعي من allauth (مثل البريد المؤكد إذا كان مطلوباً)
        super().confirm_login_allowed(user)