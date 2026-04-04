from django.shortcuts import redirect
# applications/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import JoinTrainingOpportunity
from students.models import StudentProfile
from training_entities.models import TrainingOpportunity
from core.utils import calculate_match_score


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
    # جلب الفرصة
    opportunity = get_object_or_404(TrainingOpportunity, id=opportunity_id)

    # جلب بروفايل الطالب المرتبط بالمستخدم الحالي
    try:
        student = request.user.student_profile  # استخدام الـ related_name أفضل
    except AttributeError:
        messages.error(request, "يجب إكمال ملف الطالب أولاً.")
        return redirect('students:complete_profile')

    # التأكد من عدم التكرار
    exists = JoinTrainingOpportunity.objects.filter(
        student=student,
        opportunity=opportunity
    ).exists()

    if exists:
        messages.warning(request, "لقد قمت بالتقديم مسبقاً.")
        return redirect('training_entities:opportunity_detail', id=opportunity.id)

    # حساب السكور باستخدام الدالة المركزية في core
    match_score = calculate_match_score(student, opportunity)

    # إنشاء الطلب
    JoinTrainingOpportunity.objects.create(
        student=student,
        opportunity=opportunity,
        match_score=match_score,
        status=JoinTrainingOpportunity.Status.PENDING
    )

    messages.success(request, f"تم التقديم بنجاح! نسبة المطابقة: {match_score}%")
    return redirect('training_entities:opportunity_detail', id=opportunity.id)