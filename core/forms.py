from django import forms
from django.core.exceptions import ValidationError
from .models import Country, Region, City


class CoreModelForm(forms.ModelForm):
    """
    المرجع الأساسي (Abstract-like Base Form):
    يجمع بين تنسيقات Tailwind CSS ونظام التحقق في Django.
    """
    # كلاسات الحالة العادية (Design System)
    base_classes = (
        "bg-base text-content border border-stroke-soft px-4 py-2 mt-1 rounded-lg "
        "focus:ring-2 transition duration-200 outline-none w-full shadow-sm"
    )

    # كلاسات التنبيه عند الخطأ
    error_classes = "border-red-500 focus:ring-red-500 text-red-600"

    class Meta:
        # جعلها فارغة لأن هذا الكلاس "قالب" فقط
        model = None
        fields = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # تطبيق النظام التصميمي فور الإنشاء
        self.apply_design_system()

    def apply_design_system(self):
        for field_name, field in self.fields.items():
            # 1. الحفاظ على أي كلاسات تمت إضافتها يدوياً في الـ widgets
            existing = field.widget.attrs.get('class', '')

            # 2. بناء قائمة الكلاسات بناءً على حالة الحقل (صحيح أم يحتوي خطأ)
            current_classes = self.base_classes
            if self.errors.get(field_name):
                current_classes += f" {self.error_classes}"

            # 3. دمج الكلاسات وتحديث الحقل
            field.widget.attrs['class'] = f"{existing} {current_classes}".strip()






class CountryForm(CoreModelForm):
    class Meta:
        model = Country
        fields = ['name', 'code']

class RegionForm(CoreModelForm):
    class Meta:
        model = Region
        fields = ['name', 'code','country']

class CityForm(CoreModelForm):
    class Meta:
        model = City
        fields = ['name', 'region']




# ---------------------------------------------------------
# الكلاس المرجعي العام (النموذج المثالي)
# ---------------------------------------------------------
"""

class BaseUniversalModelForm(forms.ModelForm):
    '''
    هذا الكلاس يمثل الهيكل الكامل لأي ModelForm في Django.
    يُستخدم كمرجع لفهم (الوراثة، الإعدادات، التحقق، والحفظ).
    '''

    # 1. تعريف حقول إضافية (ليست في قاعدة البيانات)
    # تُستخدم لأغراض التحقق أو التأكيد (مثل: أوافق على الشروط)
    extra_field = forms.BooleanField(
        label="أوافق على الشروط والأحكام",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    # الكلاس الداخلي class Meta
    #         هذا هو "دليل التشغيل" الخاص بالنموذج. هو لا يحتوي على منطق برمجى، بل على إعدادات:
    #         
    #         model: تحديد الجدول الذي سيتعامل معه النموذج.
    #         
    #         fields: تحديد الحقول التي تظهر للمستخدم. (استخدم __all__ لكل الحقول، أو قائمة ['field1', 'field2'] للتخصيص).
    #         
    #         exclude: الحقول التي تريد إخفاءها ومنع تعديلها.
    #         
    #         widgets: لتغيير شكل الحقل في HTML (مثلاً تحويل نص عادي إلى تقويم أو قائمة منسدلة).
    #         
    #         labels: لتغيير النص الظاهر بجانب الحقل (مثلاً بدل first_name يظهر "الاسم الأول").
    #         
    #         help_texts: إضافة ملاحظات صغيرة أسفل الحقول لإرشاد المستخدم.
            
    class Meta:
        # 2. الربط بالموديل (يجب تغييره حسب الموديل الخاص بك)
        model = None  # هنا نضع اسم الموديل المستهدف (مثلاً: CustomUser)

        # 3. تحديد الحقول:
        # - استخدم '__all__' لجلب كل الحقول
        # - أو قائمة ['field1', 'field2'] لتحديد حقول معينة
        fields = '__all__'

        # 4. الـ Widgets (المتحكمات البصرية):
        # تستخدم لتغيير نوع الإدخال في HTML (تاريخ، كلمة سر، قائمة منسدلة)
        widgets = {
            'password': forms.PasswordInput(),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

        # 5. الـ Labels (العناوين):
        # لتغيير الأسماء التي تظهر للمستخدم بجانب خانة الإدخال
        labels = {
            'username': 'اسم المستخدم الفريد',
        }
        
        

    def __init__(self, *args, **kwargs):
       '''
        6. الدالة المُنشئة (__init__):
        تعمل فور استدعاء الكلاس. نستخدمها لتعديل الحقول "ديناميكياً".
       '''
        super().__init__(*args, **kwargs)

        # حلقة تكرارية لإضافة تنسيق CSS (Bootstrap) لكل الحقول دفعة واحدة
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        # مثال لتغيير خاصية حقل معين برمجياً
        if 'email' in self.fields:
            self.fields['email'].help_text = "يرجى إدخال بريد إلكتروني صالح."
            
   def clean(self):
       # لتحقق العام  وداخلها نتحقق من الحقل او الحقول التي نريدها
        
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
    
        if password != confirm_password:
            raise forms.ValidationError("كلمتا السر غير متطابقتين!")
        
    def clean_field_name(self):
       # اذا اردناء انشاء دالة تحقق  لحقل معين  يجب تن نتبع نمط التسمية بحيث يبداء اسم الدالة بكلمة clean_ ثم اسم الحقل
       '''
        7. التحقق الخاص (Custom Validation):
        - يجب استبدال 'field_name' باسم الحقل الفعلي (مثل: clean_email).
        - تُستخدم لمنطق معقد (مثل: التأكد من أن الرقم يبدأ بكود معين).
        '''
        data = self.cleaned_data.get('field_name')
        # منطق التحقق هنا...
        # if not data_valid: raise ValidationError("رسالة الخطأ")
        return data

    def save(self, commit=True):
        ''' 
        8. دالة الحفظ (Save Method):
        المحطة الأخيرة للبيانات قبل دخولها قاعدة البيانات.
       '''
        # استخراج الكائن (Object) من الفورم بدون حفظه نهائياً (commit=False)
        instance = super().save(commit=False)

        # هنا يمكنك إضافة منطق (مثل: تحويل الاسم لحروف كبيرة قبل الحفظ)
        # instance.name = instance.name.upper()

        if commit:
            instance.save()  # الحفظ الفعلي في قاعدة البيانات
        return instance
"""
# ---------------------------------------------------------
# كيفية الاستخدام في الـ Views (منطق العمل)
# ---------------------------------------------------------
"""
في الـ View:
1. للإنشاء: form = BaseUniversalModelForm(request.POST)
2. للتعديل: form = BaseUniversalModelForm(request.POST, instance=object_name)

أهمية 'instance': 
بدونها سيقوم Django دائماً بإنشاء سجل جديد (Insert). 
معها سيقوم بتعديل السجل الموجود (Update).
"""


# 1. كلاس التنسيق (نظيف تماماً من أي وراثة ModelForm)
# class CoreModelForm(forms.ModelForm):
#     tailwind_fields_classes = (
#         " bg-base text-content border border-stroke-soft px-4 py-2 mt-1 rounded-lg "
#         "focus:ring-2 transition duration-200 outline-none w-full"
#     )
#
#     def apply_tailwind_styles(self):
#         for field in self.fields.values():
#             existing_classes = field.widget.attrs.get('class', '')
#             field.widget.attrs.update({
#                 'class': f"{existing_classes} {self.tailwind_fields_classes}".strip()
#             })


