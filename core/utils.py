# students/utils.py
from django.utils import timezone

def current_date():
    # الحصول على التاريخ والوقت الحالي (بناءً على TIME_ZONE في الإعدادات)
    # current_datetime = timezone.now()
    # الحصول على التاريخ فقط
    current_date = timezone.now().date()

    return current_date
def is_current_date_active(start_date, end_date):
    """
    تحقق ما إذا كان التاريخ الحالي يقع بين تاريخ البدء والانتهاء.
    """
    # الحصول على تاريخ اليوم (بدون الوقت للمقارنة الدقيقة للتاريخ)
    today = timezone.now().date()
    # التحقق من أن التاريخ الحالي أكبر من أو يساوي البداية
    # وأصغر من أو يساوي النهاية
    if start_date <= today <= end_date:
        return True
    return False




def  calculate_match_score(student, opportunity):

    score = 0.0
    try:
        # Ensuring data availability and avoiding duplicate queries (Optimization)
        opp_skills_qs = opportunity.required_skills.all()
        std_skills_qs = student.skills.all()

        if opp_skills_qs.exists() and std_skills_qs.exists():
            # Converting data into sets (O(n) for quick comparison
            opp_skills = {str(s.name).strip().lower() for s in opp_skills_qs if s.name}
            std_skills = {str(s.name).strip().lower() for s in std_skills_qs if s.name}

            if opp_skills:
                matches = opp_skills.intersection(std_skills)
                match_ratio = len(matches) / len(opp_skills)

                # Applying relative weight (60%)
                score += (match_ratio * 60)

                # Full Match Bonus
                if match_ratio == 1.0:
                    score += 10
    except (AttributeError, TypeError) as e:
        print(f"Error calculating skills: {e}")
        pass

    # 2. Specialization Logic (30 marks)
    # Check for specializations first to avoid NoneType errors

    student_major = getattr(student, 'major', None)
    opportunity_major = getattr(opportunity, 'major', None)

    if student_major and opportunity_major:
        if student_major == opportunity_major:
            score += 30
    elif not opportunity_major:
        # If the opportunity does not require a specific specialization
        score += 15

    # 3. Rate Logic (10 marks)
    # Use of secure numerical value verification
    try:
        if opportunity.min_gpa is not None and student.gpa is not None:
            std_gpa = float(student.gpa)
            min_gpa = float(opportunity.min_gpa)

            if std_gpa >= min_gpa:
                # Motivation Equation: Each additional point gives bonus points up to a maximum of 10
                bonus = min((std_gpa - min_gpa) * 5, 10)
                score += bonus
    except (ValueError, TypeError):
        pass

    # Final result: Rounded to one decimal place and guaranteed not to exceed 100%
    return min(round(float(score), 1), 100.0)


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








