from django.shortcuts import redirect
from functools import wraps

from core.routes import Routes


def student_required(view_func):
    """
    هذه هي الخاصية التي ستوضع فوق الدالة.
    تقوم بالتحقق: إذا لم يكن جهة تدريب، يتم التوجيه للرئيسية.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect(Routes.LOGIN)

        if not request.user.is_student:
            return redirect(Routes.HOME)

        return view_func(request, *args, **kwargs)


    return _wrapped_view