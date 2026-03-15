from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from core.routes import Routes


def training_entity_required(view_func):
    """التحقق الأساسي: هل هو جهة تدريب؟"""

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # التأكد من تسجيل الدخول
        if not request.user.is_authenticated:
            return redirect(Routes.LOGIN)

        # التأكد من نوع الحساب
        if not getattr(request.user, 'is_training_entity', False):
            messages.error(request, "هذه الصفحة مخصصة لجهات التدريب فقط.")
            return redirect(Routes.HOME)

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def training_entity_approval_required(view_func):
    @training_entity_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_approved_entity:
            return view_func(request, *args, **kwargs)

        messages.warning(request, "هذه الصفحة تتطلب موافقة الإدارة.")
        return redirect(Routes.HOME)

    return _wrapped_view

# def training_entity_required(view_func):
#     """
#     هذه هي الخاصية التي ستوضع فوق الدالة.
#     تقوم بالتحقق: إذا لم يكن جهة تدريب، يتم التوجيه للرئيسية.
#     """
#
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#
#         if not request.user.is_authenticated:
#             return redirect(Routes.LOGIN)
#
#         if not request.user.is_training_entity:
#             return redirect(Routes.HOME)
#
#
#         return view_func(request, *args, **kwargs)
#
#     return _wrapped_view
#
# def training_entity_approval_required(view_func):
#     """
#     هذه هي الخاصية التي ستوضع فوق الدالة.
#     تقوم بالتحقق: إذا لم يكن جهة تدريب، يتم التوجيه للرئيسية.
#     """
#
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#
#         if not request.user.is_authenticated:
#             return redirect(Routes.LOGIN)
#
#         if not request.user.is_training_entity or not request.user.profile.training_profile.is_available:
#             return redirect(Routes.HOME)
#
#
#         return view_func(request, *args, **kwargs)
#
#     return _wrapped_view