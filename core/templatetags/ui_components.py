from django import template

register = template.Library()


""" takes_context=True:
للسماح للمكون بالوصول إلى سياق الصفحة (Context)،
مما يتيح التحقق من حالة المستخدم (Logged-in)، الصلاحيات (Permissions)،
  أو بيانات الطلب (Request) دون تمريرها يدوياً.
"""



@register.inclusion_tag('core/components/user-card.html')
def user_card(name, email,user_id=None, image_url=None,redirect_link=None):
    default_img = "/static/images/default-avatar.png" # رابط افتراضي من تطبيق theme
    return {
        'name': name,
        'email': email,
        'image': image_url if image_url else default_img,
        'id': user_id or '000',
        'redirect_link': redirect_link or '',
    }

@register.inclusion_tag('core/components/plan-card.html', takes_context=True)
def plan_card(context, title, price, features=[], is_popular=False, button_text="Subscribe"):
    return {
        'title': title,
        'price': price,
        'features': features, # مصفوفة من المميزات
        'is_popular': is_popular,
        'button_text': button_text,
        'LANGUAGE_BIDI': context.get('LANGUAGE_BIDI'),
    }
@register.inclusion_tag('core/components/submit-button.html',name='submit-button', takes_context=True)
def submit_button(context,label, content_color=None,icon=None,bg_color=None):

    return {
        'label': label,
        'icon': icon ,
        'content_color': content_color ,
        'bg_color': bg_color ,
        'LANGUAGE_BIDI': context.get('LANGUAGE_BIDI'),
    }


@register.inclusion_tag('core/components/input-text.html',name='input-text', takes_context=True)
def input_text(context, label, name, type='text', id=None, value=None, error=None,
               content_color='text-content', icon=None, bg_color='bg-field-base',
               placeholder='', help_text=None,required=False):


    """
    مكون إدخال نصي احترافي يدعم الثيمات التلقائية (Dark/Light) عبر Tailwind 4.
    """
    formatted_error = None
    if error:
        if isinstance(error, (list, tuple)):
            formatted_error = error[0]  # نأخذ أول رسالة خطأ فقط لجمالية التصميم
        else:
            formatted_error = str(error)

    return {
        'label': label,
        'type': type,
        'name': name,
        'id': id if id else f"id_{name}",  # توليد ID تلقائي في حال عدم وجوده لضمان ربط الـ Label
        'value': value if value else '',
        'error': formatted_error,
        'icon': icon,
        'placeholder': placeholder,
        'help_text': help_text,
        'required': required,
        # ألوان تعتمد على متغيراتك الثابتة
        'bg_color': bg_color,
        'content_color': content_color,
        'request': context.get('request'), # لتمرير السياق إذا احتجت له مستقبلاً
    }



@register.inclusion_tag('core/components/input-checkbox.html', name='input-checkbox')
def input_checkbox(label, name, checked=False, required=False, id=None, error=None):
    return {
        'label': label,
        'name': name,
        'checked': checked,
        'required': required,
        'id': id if id else f"id_{name}",
        'error': error,
    }