from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from core.routes import Routes


class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # تنفيذ التحقق فقط للمستخدمين المسجلين وليس لمسؤولي النظام (Superusers)
        if request.user.is_authenticated and not request.user.is_superuser:
            user = request.user

            # 1. قائمة المسارات المستثناة لمنع التوجيه اللانهائي
            # تشمل صفحات إكمال البيانات، تسجيل الخروج، والملفات الثابتة
            excluded_paths = [
                reverse(Routes.STUDENT_COMPLETE_PROFILE),
                reverse(Routes.TRAINING_ENTITY_COMPLETE_PROFILE),
                reverse(Routes.WAITING_APPROVAL),
                reverse(Routes.LOGOUT),
                '/admin/',
                '/static/',
                '/media/',
            ]

            # إذا كان المسار الحالي ليس من المسارات المستثناة
            if not any(request.path.startswith(path) for path in excluded_paths):

                # استخدام الخاصية الديناميكية profile من موديل CustomUser الخاص بك
                profile = user.profile

                # التحقق إذا كان المستخدم "طالب"
                if user.is_student:
                    # نتحقق من وجود البروفايل واكتمال الحقول الأكاديمية والمهنية
                    if not profile or not profile.is_profile_complete:
                        # ملاحظة: يفضل إضافة property في موديل الطالب باسم is_profile_complete
                        messages.info(request, _("Please complete your academic and professional profile to proceed."))
                        return redirect(Routes.STUDENT_COMPLETE_PROFILE)

                # التحقق إذا كان المستخدم "جهة تدريب"
                elif user.is_training_entity:
                    # نتحقق من بيانات المنشأة
                    if not profile or not profile.is_profile_complete:
                        messages.info(request, _("Please complete the training provider details for follow-up."))
                        return redirect(Routes.TRAINING_ENTITY_COMPLETE_PROFILE)
                    if profile and not profile.is_available:
                        messages.warning(request, _("!! Sorry, your registration request is under review.") )
                        return redirect(Routes.WAITING_APPROVAL)


        response = self.get_response(request)
        return response