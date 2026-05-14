# # students/utils.py
from applications.models import JoinTrainingOpportunity
from core.utils import current_date, calculate_match_score
from students.models import StudentProfile
from training_entities.models import TrainingOpportunity
from django.shortcuts import  get_object_or_404
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

def student_match_opportunities(request):


    student = get_object_or_404(StudentProfile, user=request.user)
    today=current_date()

    query = Q(end_date__gte=today) & (Q(major=student.major) | Q(major__isnull=True))
    if student.gpa is not None:
        query &= (Q(min_gpa__lte=student.gpa) | Q(min_gpa__isnull=True))
    else:
        query &= Q(min_gpa__isnull=True)


    potential_opportunities = TrainingOpportunity.objects.filter(query)\
        .prefetch_related('required_skills','provider').distinct()

    results = []
    for opp in potential_opportunities:


        application = JoinTrainingOpportunity.objects.filter(student=student, opportunity=opp).first()
        std_opp_status=None
        if application :
            std_opp_status=application.status
        # استدعاء الدالة العامة للحساب
        match_percent = calculate_match_score(student, opp)

        # print("match_percent:")
        # print(match_percent)

        # احتفظ بشرط الحد الأدنى للعرض (25%)
        if match_percent > 30:
            results.append({
                'opportunity': opp,
                'status': std_opp_status,
                'score': round(match_percent, 1)
            })

    results.sort(key=lambda x: x['score'], reverse=True)

    return results


# def calculate_match_score(student, opportunity):
#     """
#     دالة عامة تحسب نسبة المطابقة وتعيد رقماً فقط (Score).
#     """
#     score = 0
#
#     # منطق حساب المهارات (60 درجة)
#     try:
#         opp_skills_qs = opportunity.required_skills.all()
#         std_skills_qs = student.skills.all()
#         if opp_skills_qs.exists() and std_skills_qs.exists():
#             opp_skills = {str(s.name).lower() for s in opp_skills_qs if s.name}
#             std_skills = {str(s.name).lower() for s in std_skills_qs if s.name}
#             if opp_skills:
#                 matches = opp_skills.intersection(std_skills)
#                 match_ratio = len(matches) / len(opp_skills)
#                 score += (match_ratio * 60)
#                 if match_ratio == 1:
#                     score += 10
#     except:
#         pass
#
#     # منطق التخصص (30 درجة)
#     if student.major and opportunity.major and student.major == opportunity.major:
#         score += 30
#     elif not opportunity.major:
#         score += 15
#
#     # منطق المعدل (10 درجات)
#     if opportunity.min_gpa is not None and student.gpa is not None:
#         if student.gpa >= opportunity.min_gpa:
#             bonus = min(float(student.gpa - opportunity.min_gpa) * 5, 10)
#             score += bonus
#
#     return min(round(float(score), 1), 100.0)