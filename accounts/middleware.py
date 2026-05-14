from django.shortcuts import redirect
from django.urls import reverse
from core.routes import Routes


# class RegistrationFlowMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         user = request.user
#
#         if user.is_authenticated and not user.is_superuser:
#             # 1. إذا كان يحتاج موافقة ولم يتم تفعيله بعد
#             if user.requires_approval:
#                 # مسموح له فقط بصفحة إكمال البيانات أو صفحة الانتظار
#                 allowed_paths = [
#                     reverse(Routes.STUDENT_COMPLETE_PROFILE),
#                     reverse(Routes.TRAINING_ENTITY_COMPLETE_PROFILE),
#                     reverse(Routes.WAITING_APPROVAL),
#                     reverse(Routes.LOGOUT),
#                 ]
#
#                 if request.path not in allowed_paths:
#                     # إذا لم يكمل بياناته بعد، أرسله للإكمال
#                     # (يمكنك فحص حقل معين مثل الهاتف أو الصورة للتأكد من الإكمال)
#                     if not user.phone_number:
#                         return redirect(Routes.STUDENT_COMPLETE_PROFILE) if user.is_student else redirect(
#                             Routes.TRAINING_ENTITY_COMPLETE_PROFILE)
#
#                     # إذا أكمل البيانات، أرسله لصفحة الانتظار
#                     return redirect(Routes.WAITING_APPROVAL)
#
#         return self.get_response(request)


# class VerificationMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         if request.user.is_authenticated:
#             # الروابط المسموح له بدخولها دائماً (صفحة البروفايل، تسجيل الخروج، صفحة الانتظار)
#             allowed_routes = [
#                 reverse(Routes.STUDENT_COMPLETE_PROFILE),
#                 reverse(Routes.TRAINING_ENTITY_COMPLETE_PROFILE),
#                 reverse(Routes.LOGOUT),
#                 reverse(Routes.WAITING_APPROVAL), # صفحة سننشئها لاحقاً
#             ]
#
#             # إذا كان الحساب غير موثق ولم يذهب لصفحة مسموحة
#             if not request.user.is_verified and request.path not in allowed_routes:
#                 # إذا لم يكمل الاسم الأول مثلاً، نرسله للإكمال
#                 if not request.user.first_name:
#                     return redirect(Routes.STUDENT_PROFILE_EDIT)
#                 # إذا أكمل البيانات ولكن لم يوافق الأدمن، نرسله لصفحة الانتظار
#                 return redirect('waiting_approval')
#
#         return self.get_response(request)