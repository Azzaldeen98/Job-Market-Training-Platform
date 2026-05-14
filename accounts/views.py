import logging
from allauth.account.utils import complete_signup
from allauth.account import app_settings
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.routes import Routes
from .forms import CustomSignupForm
from django.urls import reverse
logger = logging.getLogger(__name__)




@login_required
def redirect_by_role(request):

    dashboards = getattr(settings, 'ROLE_DASHBOARDS', {})
    default_home = getattr(settings, 'DEFAULT_HOME_URL', '/')
    identity = getattr(request.user, 'identity', None)
    role_code = getattr(identity, 'code', None) if identity else None
    target_url = dashboards.get(role_code)

    return redirect(target_url if target_url else default_home)

def error_404(request, exception):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)
def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST, request.FILES)
        if form.is_valid():
            # حفظ المستخدم عبر Allauth لضمان تشفير كلمة السر وإرسال الإيميل
            user = form.save(request)

            # هذا السطر مهم جداً! يخبر Allauth بإتمام العملية (بما في ذلك تسجيل الدخول)
            if user.is_student:
                success_url = reverse(Routes.STUDENT_COMPLETE_PROFILE)
            elif user.is_training_entity:
                success_url = reverse(Routes.TRAINING_ENTITY_COMPLETE_PROFILE)
            else:
                success_url = reverse(Routes.HOME)

            return complete_signup(
                request,
                user,
                email_verification=app_settings.EMAIL_VERIFICATION,
                success_url=success_url,
                signal_kwargs={}
            )
            # # منطق التوجيه الخاص بك
            # if user.is_student:
            #     return redirect(Routes.STUDENT_COMPLETE_PROFILE)
            # elif user.is_training_entity:
            #     return redirect(Routes.TRAINING_ENTITY_COMPLETE_PROFILE)
            #
            # return redirect(Routes.HOME)
    else:
        form = CustomSignupForm()
    return render(request, 'account/signup.html', {'form': form})
def waiting_approval_view(request):
    # إذا قام الأدمن بتفعيله وهو لا يزال فاتحاً لهذه الصفحة، نقوم بتوجيهه للرئيسية فور تحديث الصفحة
    #request.user.identity.requires_approval

    # if request.user.is_authenticated and request.user.is_verified:
    #     return redirect(Routes.HOME)

    return render(request, 'account/waiting_approval.html')


# @login_required
# def redirect_by_role(request):
#     """
#         نقطة توزيع المستخدمين (Traffic Controller):
#         - الوظيفة: توجيه المستخدم بعد تسجيل الدخول إلى لوحة التحكم الخاصة به.
#         - المرجعية: يعتمد على قاموس ROLE_DASHBOARDS المعرف في settings.py.
#         - الأمان: يستخدم getattr للتعامل مع الحالات التي قد يكون فيها الـ identity مفقوداً أو الـ Role غير معرف.
#         """
#     # 1. جلب قاموس المسارات من الإعدادات
#     dashboards = getattr(settings, 'ROLE_DASHBOARDS', {})
#
#     # 2. جلب المسار الافتراضي للموقع (ووضع 'home' كقيمة احتياطية نهائية)
#     default_home = getattr(settings, 'DEFAULT_HOME_URL', '/')
#
#     # 3. الحصول على كود الدور
#     role_code = getattr(request.user.identity, 'code', None)
#
#     # 4. محاولة التوجيه بناءً على الدور
#     target_url = dashboards.get(role_code)
#     # le_code = None
#     if request.user.identity:
#         role_code = request.user.identity.code  # جلب الكود من جدول الـ Role
#
#     print(f"DEBUG: User Role Code is: {role_code}")  # سطر للتحقق في الـ Terminal
#
#     # target_url = dashboards.get(role_code)
#     logger.log(f"URL:{target_url}")
#
#     if target_url:
#         return redirect(target_url)
#
#
#
#     # 5. التوجيه للمسار الافتراضي إذا لم يوجد دور أو مسار مخصص
#     return redirect(default_home)




# def signup(request):
#     if request.method == 'POST':
#         # هنا نستقبل البيانات المدخلة والوسائط من واجهة المستخدم
#         form = CustomSignupForm(request.POST, request.FILES)
#         #يتأكد من أن البريد الإلكتروني صحيح، كلمة المرور مطابقة للشروط، وأن المستخدم غير موجود مسبقاً.
#         if form.is_valid():
#             user = form.save(request) # تحويل كائن البيانات المدخلة الى استعلام قابل لتنفيذ في قاعدة البيانات
#             login(request, user) # تسجيل دخول تلقائي بعد التسجيل
#
#             # print(f"DEBUG:def->signup()")
#
#             if user.is_student:
#                 return redirect('students:complete_profile')
#
#             elif user.is_training_entity:
#                 return redirect('training_entities:complete_profile')
#
#             return redirect(Routes.HOME) # الانتقال لصفحة الرئيسية
#     else:
#         form = CustomSignupForm()
#     return render(request, 'account/signup.html', {'form': form})






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
