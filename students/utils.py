# # students/utils.py
#
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