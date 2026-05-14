from django.shortcuts import redirect
# applications/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import JoinTrainingOpportunity
from students.models import StudentProfile
from training_entities.models import TrainingOpportunity
from core.utils import calculate_match_score
from django.utils.translation import gettext_lazy as _

def view_application_details(request, application_id):
    # جلب الطلب مع البيانات المرتبطة لتحسين الأداء
    application = get_object_or_404(
        JoinTrainingOpportunity.objects.select_related('student__user', 'opportunity'),
        id=application_id
    )

    return render(request, 'training_entities/opportunities/application_review.html', {
        'application': application  # تأكد من تفعيل هذا السطر لكي تظهر البيانات في HTML
    })


def join_opportunity(request, opportunity_id):
    # 1. جلب الفرصة
    opportunity = get_object_or_404(TrainingOpportunity, id=opportunity_id)

    # 2. تحديد الـ Namespace بشكل آمن
    # يفضل استخدامه بالجمع 'students' إذا كان هذا هو المسجل في urls.py
    app = "students"

    # 3. جلب كائن الطالب الحقيقي (Object) وليس النص
    try:
        # تأكد أنك تجلب البروفايل الفعلي
        student = request.user.profile

        if not request.user.is_student:
            messages.error(request, _("This procedure is available to students only."))
            return redirect('core:home')

    except AttributeError:
        messages.error(request, _("The student file must be completed first."))
        return redirect(f'{app}:complete_profile')

    # 4. التأكد من عدم التكرار (باستخدام كائن student الحقيقي)
    exists = JoinTrainingOpportunity.objects.filter(
        student=student,
        opportunity=opportunity
    ).exists()

    if exists:
        messages.warning(request, _('Pre-applied'))
        return redirect(f'{app}:opportunity_detail', id=opportunity.id)

    # 5. حساب السكور (نمرر الكائنات Objects)
    match_score = calculate_match_score(student, opportunity)

    # 6. إنشاء الطلب
    JoinTrainingOpportunity.objects.create(
        student=student,
        opportunity=opportunity,
        match_score=match_score,
        status=JoinTrainingOpportunity.Status.PENDING
    )

    messages.success(request, f"{_('Application successful! Match rate')} : {match_score}%")

    # 7. التوجيه النهائي (تأكد من وجود حرف s في students)
    return redirect(f'{app}:opportunity_detail', id=opportunity.id)

def cancel_join_opportunity(request, opportunity_id):
    # 1. جلب الطلب والتأكد أن المستخدم الحالي هو صاحب الطلب (أمان إضافي)
    # نستخدم filter ثم first لتجنب الانهيار في حال عدم وجود الطلب
    join_request = JoinTrainingOpportunity.objects.filter(
        student=request.user.profile,
        opportunity_id=opportunity_id,
        # status=JoinTrainingOpportunity.Status.PENDING
    ).first()

    if join_request:
        # 2. حذف الطلب
        join_request.delete()
        messages.success(request, _("The application to join has been successfully cancelled"))
    else:
        messages.error(request, _("Sorry, this request cannot be canceled or it does not exist"))

    # 3. التوجيه للجهة الصحيحة (تأكد من استخدام 'students' بالجمع)
    return redirect('students:opportunity_detail', id=opportunity_id)
# def join_opportunity(request, opportunity_id):
#     # جلب الفرصة
#     opportunity = get_object_or_404(TrainingOpportunity, id=opportunity_id)
#
#     # جلب بروفايل الطالب المرتبط بالمستخدم الحالي
#     try:
#         student = request.user.profile  # استخدام الـ related_name أفضل
#     except AttributeError:
#         messages.error(request, "يجب إكمال ملف الطالب أولاً.")
#         return redirect('students:complete_profile')
#
#     # التأكد من عدم التكرار
#     exists = JoinTrainingOpportunity.objects.filter(
#         student=student,
#         opportunity=opportunity
#     ).exists()
#
#     if exists:
#         messages.warning(request, "لقد قمت بالتقديم مسبقاً.")
#         return redirect('training_entities:opportunity_detail', id=opportunity.id)
#
#     # حساب السكور باستخدام الدالة المركزية في core
#     match_score = calculate_match_score(student, opportunity)
#
#     # إنشاء الطلب
#     JoinTrainingOpportunity.objects.create(
#         student=student,
#         opportunity=opportunity,
#         match_score=match_score,
#         status=JoinTrainingOpportunity.Status.PENDING
#     )
#
#     messages.success(request, f"تم التقديم بنجاح! نسبة المطابقة: {match_score}%")
#     return redirect('training_entities:opportunity_detail', id=opportunity.id)