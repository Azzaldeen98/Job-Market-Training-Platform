from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomSignupForm

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def redirect_by_role(request):
    """
        نقطة توزيع المستخدمين (Traffic Controller):
        - الوظيفة: توجيه المستخدم بعد تسجيل الدخول إلى لوحة التحكم الخاصة به.
        - المرجعية: يعتمد على قاموس ROLE_DASHBOARDS المعرف في settings.py.
        - الأمان: يستخدم getattr للتعامل مع الحالات التي قد يكون فيها الـ identity مفقوداً أو الـ Role غير معرف.
        """
    # 1. جلب قاموس المسارات من الإعدادات
    dashboards = getattr(settings, 'ROLE_DASHBOARDS', {})

    # 2. جلب المسار الافتراضي للموقع (ووضع 'home' كقيمة احتياطية نهائية)
    default_home = getattr(settings, 'DEFAULT_HOME_URL', '/')

    # 3. الحصول على كود الدور
    role_code = getattr(request.user.identity, 'code', None)

    # 4. محاولة التوجيه بناءً على الدور
    target_url = dashboards.get(role_code)
    le_code = None
    if request.user.identity:
        role_code = request.user.identity.code  # جلب الكود من جدول الـ Role

    print(f"DEBUG: User Role Code is: {role_code}")  # سطر للتحقق في الـ Terminal

    # target_url = dashboards.get(role_code)

    if target_url:
        return redirect(target_url)



    # 5. التوجيه للمسار الافتراضي إذا لم يوجد دور أو مسار مخصص
    return redirect(default_home)

def error_404(request, exception):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)


# دالة تسجيل حساب وضيفتها:
# التحقق من نوع دالة الارسال  post | get  او غيرها
# إلتقاط البيانات من الطلب والمدخله في النموذج من قبل المستخدم
# def register(request):
#     if request.method == 'POST':
#         # هنا نستقبل البيانات المدخلة والوسائط من واجهة المستخدم
#         form = CustomSignupForm(request.POST, request.FILES)
#         #يتأكد من أن البريد الإلكتروني صحيح، كلمة المرور مطابقة للشروط، وأن المستخدم غير موجود مسبقاً.
#         if form.is_valid():
#             user = form.save() # تحويل كائن البيانات المدخلة الى استعلام قابل لتنفيذ في قاعدة البيانات
#             login(request, user) # تسجيل دخول تلقائي بعد التسجيل
#             return redirect('core:home') # الانتقال لصفحة الرئيسية
#     else:
#         form = CustomSignupForm()
#     return render(request, 'account/register.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        # هنا نستقبل البيانات المدخلة والوسائط من واجهة المستخدم
        form = CustomSignupForm(request.POST, request.FILES)
        #يتأكد من أن البريد الإلكتروني صحيح، كلمة المرور مطابقة للشروط، وأن المستخدم غير موجود مسبقاً.
        if form.is_valid():
            user = form.save() # تحويل كائن البيانات المدخلة الى استعلام قابل لتنفيذ في قاعدة البيانات
            login(request, user) # تسجيل دخول تلقائي بعد التسجيل
            return redirect('core:home') # الانتقال لصفحة الرئيسية
    else:
        form = CustomSignupForm()
    return render(request, 'account/signup.html', {'form': form})

# def search_users(request):
#     query = request.GET.get('search', '')
#     if query:
#         users = CustomUser.objects.filter(username__icontains=query)
#     else:
#         users = []
#
#     # نرسل ملف HTML صغير جداً يحتوي فقط على القائمة
#     return render(request, 'core/home.html', {'users': users})
#
