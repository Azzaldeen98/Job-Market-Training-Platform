from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import *
from allauth.account import forms as allauth_forms
from django.utils.translation import gettext_lazy as _
from allauth.account.forms import SignupForm



# 1. كلاس التنسيق (نظيف تماماً من أي وراثة ModelForm)
class BaseStyledForm:
    tailwind_fields_classes = (
        " bg-base text-content border border-stroke-soft px-4 py-2 mt-1 rounded-lg "
        "focus:ring-2 transition duration-200 outline-none w-full"
    )

    def apply_tailwind_styles(self):
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs.update({
                'class': f"{existing_classes} {self.tailwind_fields_classes}".strip()
            })


# 2. الكلاس الموحد والنهائي (استخدم هذا الاسم فقط)
class CustomSignupForm(SignupForm, BaseStyledForm):
    first_name = forms.CharField(max_length=150, label='First Name')
    last_name = forms.CharField(max_length=150, label='Last Name')
    identity = forms.ModelChoiceField(
        queryset=Role.objects.filter(view_in_register=True, is_identity=True),
        label="Account Type",
        empty_label="--- Select account type ---",
        required=True
    )

    def __init__(self, *args, **kwargs):
        # تشغيل الـ init الخاص بـ Allauth
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].widget = forms.HiddenInput()
            self.fields['username'].required = False
        # تطبيق تنسيق Tailwind على كل الحقول (بما فيها الباسورد والايميل)
        self.apply_tailwind_styles()

    def save(self, request):
        email=self.cleaned_data.get('email')
        self.cleaned_data['username']=email
        # حفظ المستخدم عبر Allauth أولاً
        user = super(CustomSignupForm, self).save(request)

        # حفظ الحقول الإضافية في موديل CustomUser
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.identity = self.cleaned_data['identity']

        user.save()
        return user


# class CustomSignupForm(allauth_forms.SignupForm):
#     first_name = forms.CharField(max_length=150, label='First Name')
#     last_name = forms.CharField(max_length=150, label='Last Name')
#
#     identity = forms.ModelChoiceField(
#         queryset=Role.objects.filter(view_in_register=True, is_identity=True),
#         label="Account Type"
#     )
#
#     def save(self, request):
#         user = super(CustomSignupForm, self).save(request)
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.identity = self.cleaned_data['identity']
#         user.save()
#         return user
#
#
# class BaseStyledForm(forms.ModelForm):
#     tailwind_fields_classes = (
#         " bg-base text-content border border-stroke-soft px-4 py-2 mt-1 rounded-lg "
#         "focus:ring-2 transition duration-200 outline-none"
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs.update({'class': self.tailwind_fields_classes + " w-full"})
#
#     # تأكد من الوراثة من SignupForm الخاص بـ Allauth لتجنب خطأ try_save
#
#
# class CustomUserCreationForm(SignupForm, BaseStyledForm):
#     # تعريف الحقول الإضافية يدوياً هنا لأن SignupForm لا يقرأ Meta model
#     first_name = forms.CharField(max_length=30, label="First Name")
#     last_name = forms.CharField(max_length=30, label="Last Name")
#     identity = forms.ModelChoiceField(
#         queryset=Role.objects.filter(is_identity=True, view_in_register=True),
#         label="Account type",
#         empty_label="--- Select account type ---",
#         required=True
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # تطبيق تنسيق Tailwind الخاص بك
#         for field_name in ['first_name', 'last_name', 'identity']:
#             if field_name in self.fields:
#                 self.fields[field_name].widget.attrs.update({
#                     'class': self.tailwind_fields_classes
#                 })
#
#     def save(self, request):
#         # 1. دع Allauth تنشئ المستخدم الأساسي (الإيميل، الباسورد، اليوزرنيم)
#         user = super(CustomUserCreationForm, self).save(request)
#
#         # 2. حفظ الحقول الإضافية الخاصة بك في موديل CustomUser
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.identity = self.cleaned_data['identity']
#
#         user.save()
#         return user



# from  config.settings import TAILWIND_FIELD_CLASSES

# class CustomUserCreationForm(UserCreationForm):
#     # نحدد الmodel  الذي سيرتبط بنموذج الادخال بالواجهة والحقول التي ستظهر
#     # يعتب هذا الكلاس مولد ذكي للحقول في الواجهة دون  الحاجة لكتابة وسوم الادخال بواسطة html
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         # الحقول التي تريد من المستخدم تعبئتها عند التسجيل
#         fields = UserCreationForm.Meta.fields + ('email', 'profile_picture', 'bio',)
#         widgets = {
#             'email': forms.EmailInput(attrs={
#                 'class': 'custom-input',
#                 'placeholder': _('example@domain.com'),  # تصحيح: الـ placeholder للإيميل يجب أن يكون إيميلاً وليس اسماً
#                 'autocomplete': 'email'
#             }),
#             'phone_number': forms.TextInput(attrs={
#                 'class': 'custom-input',
#                 'placeholder': _('e.g., +966500000000'),
#             }),
#             'bio': forms.Textarea(attrs={
#                 'class': 'custom-textarea',
#                 'rows': 3,
#                 'placeholder': _('Tell us a little about yourself...')
#             }),
#             'birth_date': forms.DateInput(attrs={
#                 'class': 'custom-input',
#                 'type': 'date'  # لتحويل الحقل لمختار تاريخ (Date Picker) في المتصفح
#             }),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # هذه الحلقة تمر على "كل" الحقول بدون استثناء وتضيف لها الكلاس المطلوب
#         for field_name, field in self.fields.items():
#             # إضافة الكلاس مع الحفاظ على أي كلاسات موجودة مسبقاً
#             existing_classes = field.widget.attrs.get('class', '')
#             field.widget.attrs['class'] = f'{existing_classes} custom-input'.strip()
#
#             # اختياري: إضافة placeholder تلقائي لاسم المستخدم إذا لم يوجد
#             if field_name == 'username':
#                 field.widget.attrs['placeholder'] = _('Enter your username')
#



# class BaseStyledForm(forms.ModelForm):
#     # نضع كلاسات Tailwind هنا لسهولة تغييرها في كل الموقع لاحقاً
#     tailwind_classes = (
#         "w-full px-4 py-2 mt-1 border border-gray-300 rounded-lg shadow-sm "
#         "focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-700 "
#         "transition duration-200 outline-none"
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.apply_custom_style()
#
#     def apply_custom_style(self):
#         for field in self.fields.values():
#             # إضافة التنسيقات لكل حقل
#             field.widget.attrs.update({
#                 'class': self.tailwind_classes,
#                 'placeholder': field.label  # إضافة placeholder تلقائي من اسم الحقل
#             })




# class BaseStyledForm2(forms.ModelForm):
#     # تعريف كلاسات Tailwind الشاملة (نهاري + ليلي + تفاعلي)
#     standard_classes = (
#         "block w-full px-4 py-2.5 text-base font-normal transition duration-200 ease-in-out "
#         "bg-white dark:bg-gray-800 "  # الخلفية
#         "text-gray-900 dark:text-gray-100 "  # لون النص
#         "border border-gray-300 dark:border-gray-600 rounded-lg "  # الإطار
#         "focus:border-blue-500 dark:focus:border-blue-400 "  # لون الإطار عند التركيز
#         "focus:ring-2 focus:ring-blue-500/20 "  # حلقة مضيئة خفيفة (Shadow ring)
#         "outline-none shadow-sm "
#         "placeholder-gray-400 dark:placeholder-gray-500"  # لون النص المؤقت
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.apply_professional_styles()
#
#     def apply_professional_styles(self):
#         for field_name, field in self.fields.items():
#             # 1. تطبيق الكلاسات الأساسية
#             field.widget.attrs.update({'class': self.standard_classes})
#
#             # 2. إضافة Placeholder تلقائي إذا لم يكن موجوداً
#             if not field.widget.attrs.get('placeholder'):
#                 field.widget.attrs['placeholder'] = field.label
#
#             # 3. تخصيص حقول معينة
#             if isinstance(field.widget, forms.Textarea):
#                 field.widget.attrs.update({'rows': '3', 'class': self.standard_classes + ' resize-none'})
#
#             elif isinstance(field.widget, forms.CheckboxInput):
#                 field.widget.attrs.update({
#                     'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
#                 })
#
#             elif isinstance(field.widget, forms.FileInput):
#                 field.widget.attrs.update({
#                     'class': (
#                         "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 "
#                         "dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 "
#                         "file:mr-4 file:py-2 file:px-4 file:rounded-l-lg file:border-0 "
#                         "file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 "
#                         "hover:file:bg-blue-100 dark:file:bg-gray-600 dark:file:text-white"
#                     )
#                 })
#



# --- 1. نموذج إنشاء الحساب ---
# class CustomUserCreationForm(BaseStyledForm, UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = ('identity','first_name', 'last_name', 'username', 'email')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         if 'first_name' in self.fields and 'last_name' in self.fields:
#             self.fields['first_name'].widget.attrs.update({'class': self.tailwind_fields_classes})
#             self.fields['last_name'].widget.attrs.update({'class': self.tailwind_fields_classes})
#
#         # 2. تخصيص حقل الهوية (Identity)
#         elif 'identity' in self.fields:
#             # جلب الأدوار التي تعمل كـ "هوية" فقط (طالب، شركة، إلخ)
#             self.fields['identity'].queryset = Role.objects.filter(is_identity=True,view_in_register=True)
#             # جعل الحقل إجبارياً عند التسجيل
#             self.fields['identity'].required = True
#             # تغيير النص الافتراضي للخيار الأول
#             self.fields['identity'].empty_label = "--- Select account type ---"
#             # Add a caption (Label)
#             self.fields['identity'].label = "Account type"




# --- 2. نموذج تعديل البيانات الأساسية (User Model) ---
class UserUpdateForm(BaseStyledForm):
    class Meta:
        model = CustomUser
        # أضفنا الجوال وتاريخ الميلاد هنا لأنك وضعتهما في BaseCustomUser
        fields = ('first_name', 'last_name', 'username','email', 'phone_number', 'birth_date')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

# --- 3. نموذج تعديل الملف الشخصي (Profile Model) ---
class ProfileUpdateForm(BaseStyledForm):
    class Meta:
        model = Profile  # التغيير الجذري هنا: نربطه بموديل Profile
        fields = ('picture', 'bio') # لاحظ الفاصلة بعد العنصر الأخير إذا كان واحداً
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'bio' in self.fields:
            self.fields['bio'].widget.attrs.update({'class': self.tailwind_fields_classes + ' w-full resize-none'})

#
# class BaseStyledForm(forms.ModelForm):
#
#     tailwind_fields_classes = ( "w-full bg-base text-content border border-stroke-soft  px-4 py-2 mt-1  rounded-lg  "
#         "focus:ring-2  transition duration-200 outline-none")
#     def __init__(self, *args, **kwargs):
#
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             # سطر واحد فقط يربط الـ Form بتنسيقات Tailwind المركزية
#             field.widget.attrs.update({'class': self.tailwind_fields_classes})
#
#
# # --- 1. نموذج إنشاء الحساب (Signup) ---
# class CustomUserCreationForm(BaseStyledForm,UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = ('username', 'email') # التسجيل السريع دائماً أفضل
#
#
#
# # --- 2. نموذج تعديل البيانات الأساسية (Account Info) ---
# # هذا النموذج لتعديل (الاسم، الإيميل) - بيانات جدول User
# class UserUpdateForm(BaseStyledForm):
#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name', 'email')
#         # widgets = {
#         #     'email': forms.EmailInput(attrs={'class': 'custom-input'}),
#         #     'first_name': forms.TextInput(attrs={'class': 'custom-input'}),
#         #     'last_name': forms.TextInput(attrs={'class': 'custom-input'}),
#         # }
#
#
# # --- 3. نموذج تعديل الملف الشخصي (Profile Info) ---
# # هذا النموذج لتعديل (الصورة، النبذة، الجوال) - بيانات جدول Profile
# class ProfileUpdateForm(BaseStyledForm):
#     class Meta:
#         model = CustomUser  # يفضل استخدام settings.AUTH_USER_MODEL في المشاريع الحقيقية
#         fields = ('picture') #, 'bio', 'phone_number', 'birth_date')
#         # widgets = {
#         #     # لاحظ أننا لم نضع كلاسات هنا، سنترك المهمة لـ BaseStyledForm
#         #     'birth_date': forms.DateInput(attrs={'type': 'date'}),
#         #     'bio': forms.Textarea(attrs={'rows': 3}),
#         # }
#
#     def __init__(self, *args, **kwargs):
#         # 1. استدعاء __init__ الخاص بـ BaseStyledForm أولاً
#         # سيقوم تلقائياً بإضافة كلاسات Tailwind لكل الحقول
#         super().__init__(*args, **kwargs)
#
#         # 2. تخصيص إضافي لبعض الحقول إذا لزم الأمر
#         if 'bio' in self.fields:
#             # إضافة كلاس لمنع تكبير حجم النص (خاص بـ Tailwind)
#             self.fields['bio'].widget.attrs.update({'class': self.tailwind_fields_classes + ' resize-none'})