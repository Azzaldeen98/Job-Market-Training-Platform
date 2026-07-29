# students/utils.py
from django.utils import timezone
import uuid
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



def calculate_match_score(student, opportunity):
    score = 0.0

    # ---------------------------------------------------------
    # 1. Skills Logic (60 + 10 Marks)
    # ---------------------------------------------------------
    try:
        opp_skills_qs = opportunity.required_skills.all()
        std_skills_qs = student.skills.all()

        if opp_skills_qs.exists() and std_skills_qs.exists():
            opp_skills = {str(s.name).strip().lower() for s in opp_skills_qs if s.name}
            std_skills = {str(s.name).strip().lower() for s in std_skills_qs if s.name}

            if opp_skills:
                matches = opp_skills.intersection(std_skills)
                match_ratio = len(matches) / len(opp_skills)
                score += (match_ratio * 60)

                if match_ratio == 1.0:
                    score += 10
    except (AttributeError, TypeError) as e:
        print(f"Error calculating skills: {e}")
        pass

    # ---------------------------------------------------------
    # 2. Specialization Logic (30 Marks) - المصلحة والآمنة
    # ---------------------------------------------------------
    student_major = getattr(student, 'major', None)
    opportunity_major = getattr(opportunity, 'major', None)

    # تحويل حالة أحرف قيمة الفرصة لتفادي مشاكل الأخطاء الإملائية (مثل All أو all)
    opp_major_str = str(opportunity_major).strip().lower() if opportunity_major else ""

    if opportunity_major and opp_major_str != "all":
        # إذا كانت الفرصة تطلب تخصصاً معيناً والتشابه متطابق تماماً
        if student_major == opportunity_major:
            score += 30
    elif opp_major_str == "all" or not opportunity_major:
        # إذا كانت الفرصة مفتوحة للجميع أو الحقل فارغ تماماً، يحصل الطالب على الـ 30 كاملة لملائمتها له
        score += 30

    # ---------------------------------------------------------
    # 3. Dynamic GPA Rate Logic (10 Marks) - المؤمن والمطور
    # ---------------------------------------------------------
    try:
        if opportunity.min_gpa is not None and student.gpa is not None:
            std_gpa_raw = float(student.gpa)
            opp_min_gpa_raw = float(opportunity.min_gpa)

            # 1. التخمين الذكي والدقيق لمقياس الطالب (في حال كان الحقل فارغاً في قاعدة البيانات)
            std_scale = getattr(student, 'gpa_scale', None)
            if std_scale is None:
                if std_gpa_raw > 5.0:
                    std_scale = 100.0  # بالتأكيد نظام مئوي (مثال: 95.5)
                elif std_gpa_raw > 4.0:
                    std_scale = 5.0    # بالتأكيد نظام من 5 (مثال: 4.5)
                else:
                    std_scale = 4.0    # آمن تكتيكياً: أي معدل 4.0 أو أقل يُعامل كنظام من 4 لحمايته
            else:
                std_scale = float(std_scale)

            # 2. التخمين الذكي لمقياس الفرصة التدريبية (في حال كان الحقل فارغاً في قاعدة البيانات)
            opp_scale = getattr(opportunity, 'gpa_scale', None)
            if opp_scale is None:
                if opp_min_gpa_raw > 5.0:
                    opp_scale = 100.0
                elif opp_min_gpa_raw > 4.0:
                    opp_scale = 5.0
                else:
                    opp_scale = 4.0
            else:
                opp_scale = float(opp_scale)

            # 3. تحويل وتوحيد المعدلات إلى نظام مئوي موحد (0% - 100%) بأمان تام
            student_percentage = (std_gpa_raw / std_scale) * 100.0
            opportunity_percentage = (opp_min_gpa_raw / opp_scale) * 100.0

            # 4. التحقق والمقارنة العادلة بعد توحيد الميزان
            if student_percentage >= opportunity_percentage:
                # معادلة التحفيز بناءً على الفارق المئوي:
                # كل 1% تقدم إضافي يمنحه 0.5 نقطة بونص، بحد أقصى 10 نقاط كاملة
                bonus = min((student_percentage - opportunity_percentage) * 0.5, 10.0)
                score += bonus

    except (ValueError, TypeError, ZeroDivisionError):
        # وضع الحماية من القسمة على صفر أو المشاكل التوافقية
        pass

    # النتيجة النهائية: مقربة ومضمونة ألا تتجاوز الـ 100%
    return min(round(float(score), 1), 100.0)

# def  calculate_match_score(student, opportunity):
#
#     score = 0.0
#     try:
#         # Ensuring data availability and avoiding duplicate queries (Optimization)
#         opp_skills_qs = opportunity.required_skills.all()
#         std_skills_qs = student.skills.all()
#
#         if opp_skills_qs.exists() and std_skills_qs.exists():
#             # Converting data into sets (O(n) for quick comparison
#             opp_skills = {str(s.name).strip().lower() for s in opp_skills_qs if s.name}
#             std_skills = {str(s.name).strip().lower() for s in std_skills_qs if s.name}
#
#             if opp_skills:
#                 matches = opp_skills.intersection(std_skills)
#                 match_ratio = len(matches) / len(opp_skills)
#
#                 # Applying relative weight (60%)
#                 score += (match_ratio * 60)
#
#                 # Full Match Bonus
#                 if match_ratio == 1.0:
#                     score += 10
#     except (AttributeError, TypeError) as e:
#         print(f"Error calculating skills: {e}")
#         pass
#
#     # 2. Specialization Logic (30 marks)
#     # Check for specializations first to avoid NoneType errors
#
#     student_major = getattr(student, 'major', None)
#     opportunity_major = getattr(opportunity, 'major', None)
#
#     if student_major and opportunity_major:
#         if student_major == opportunity_major:
#             score += 30
#     elif not opportunity_major:
#         # If the opportunity does not require a specific specialization
#         score += 15
#
#     # 3. Rate Logic (10 marks)
#     # Use of secure numerical value verification
#     try:
#         if opportunity.min_gpa is not None and student.gpa is not None:
#             std_gpa = float(student.gpa)
#             min_gpa = float(opportunity.min_gpa)
#
#             if std_gpa >= min_gpa:
#                 # Motivation Equation: Each additional point gives bonus points up to a maximum of 10
#                 bonus = min((std_gpa - min_gpa) * 5, 10)
#                 score += bonus
#     except (ValueError, TypeError):
#         pass
#
#     # Final result: Rounded to one decimal place and guaranteed not to exceed 100%
#     return min(round(float(score), 1), 100.0)











