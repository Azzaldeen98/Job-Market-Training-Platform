# students/utils.py
from django.utils import timezone

from core.utils import current_date
from training_entities.models import TrainingOpportunity


def active_opportunities(request):
    today = current_date()
    # جلب الفرص التي تاريخ انتهائها أكبر من أو يساوي اليوم
    active_opps = TrainingOpportunity.objects.filter(end_date__gte=today)

    return active_opps



# def calculate_match_score(student, opportunity):
#     """
#         دالة مركزية لحساب نسبة المطابقة.
#         تستقبل كائنات (Objects) وتقوم بمعالجة البيانات داخلياً.
#         """
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
#
#
#
# def is_opportunity_active(start_date, end_date):
#     """
#     تحقق ما إذا كان التاريخ الحالي يقع بين تاريخ البدء والانتهاء.
#     """
#     # الحصول على تاريخ اليوم (بدون الوقت للمقارنة الدقيقة للتاريخ)
#     today = timezone.now().date()
#     # التحقق من أن التاريخ الحالي أكبر من أو يساوي البداية
#     # وأصغر من أو يساوي النهاية
#     if start_date <= today <= end_date:
#         return True
#     return False