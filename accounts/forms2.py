from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Role

# ملاحظة: لا تستورد SignupForm هنا في الأعلى أبداً!

class CustomSignupForm(object):
    """
    هذا الكلاس سيتم استبدال وراثته ديناميكياً لتجنب الوراثة الدائرية
    """
    first_name = forms.CharField(max_length=150, label=_('First Name'))
    last_name = forms.CharField(max_length=150, label=_('Last Name'))
    identity = forms.ModelChoiceField(
        queryset=Role.objects.filter(view_in_register=True, is_identity=True),
        label=_("Account Type")
    )

    def save(self, request):
        # سنقوم باستدعاء save الخاص بالأب يدوياً بعد التأكد من الوراثة
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.identity = self.cleaned_data.get('identity')
        user.save()
        return user

# --- الخدعة السحرية هنا ---
from allauth.account.forms import SignupForm
# نقوم بحقن الوراثة بعد أن تم تحميل SignupForm بنجاح
CustomSignupForm.__bases__ = (SignupForm,)