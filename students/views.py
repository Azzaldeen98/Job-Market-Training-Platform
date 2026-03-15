from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from accounts.models import CustomUser
from students.decorators import student_required
from students.forms import StudentProfileForm
from students.models import StudentProfile
from core.routes import Routes
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from decimal import Decimal, InvalidOperation

from training_entities.models import TrainingOpportunity

# Create your views here.
app_name="students"

@login_required
@student_required
def dashboard(request):
    return render(request, f'{app_name}/dashboard.html')

@login_required
@student_required
def student_complete_profile(request):

    # if not request.user.is_student:
    #     return redirect(Routes.HOME)

    profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # التوجه لصفحة النجاح بعد الحفظ
            return redirect(Routes.STUDENT_DASHBOARD)
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, f'{app_name}/complete_profile.html', {'form': form})\


@login_required
@student_required
def match_opportunities(request):
    # 1. جلب بروفايل الطالب
    student = get_object_or_404(StudentProfile, user=request.user)

    # 2. الاستعلام الأولي (فلترة أساسية)
    # نجلب الفرص التي تطابق التخصص أو الفرص العامة
    query = Q(major=student.major) | Q(major__isnull=True)

    # فلترة صارمة للمعدل: إذا كان هناك معدل مطلوب، يجب أن يكون معدل الطالب أعلى منه أو يساويه
    if student.gpa is not None:
        query &= (Q(min_gpa__lte=student.gpa) | Q(min_gpa__isnull=True))
    else:
        # إذا الطالب لم يدخل معدله، نظهر له فقط الفرص التي لا تشترط معدلاً
        query &= Q(min_gpa__isnull=True)

    potential_opportunities = TrainingOpportunity.objects.filter(query).prefetch_related('required_skills').distinct()

    def calculate_match_score(std, opp):
        score = 0

        # --- [ أ. المهارات: الوزن الأكبر (60 درجة) ] ---
        skill_weight = 60
        try:
            if opp.required_skills.exists() and std.skills.exists():
                opp_skills = {str(s.name).lower() for s in opp.required_skills.all() if s.name}
                std_skills = {str(s.name).lower() for s in std.skills.all() if s.name}

                if opp_skills:
                    matches = opp_skills.intersection(std_skills)
                    match_ratio = len(matches) / len(opp_skills)
                    score += (match_ratio * skill_weight)

                    # بونص للاتقان الكامل للمهارات
                    if match_ratio == 1:
                        score += 10
        except Exception:
            pass

        # --- [ ب. التخصص: وزن متوسط (30 درجة) ] ---
        if std.major and opp.major and std.major == opp.major:
            score += 30
        elif not opp.major:  # فرص عامة
            score += 15

        # --- [ ج. المعدل: ميزة إضافية (10 درجات) ] ---
        # هنا المعدل لا يستبعد (لأن الاستبعاد تم في الكويري فوق)، بل يعطي بونص تميز
        if opp.min_gpa is not None and std.gpa is not None:
            if std.gpa >= opp.min_gpa:
                # بونص طردي: كلما زاد معدلك عن المطلوب زاد السكور قليلاً
                bonus = min(float(std.gpa - opp.min_gpa) * 5, 10)
                score += bonus

        return min(score, 100)

    # 3. بناء قائمة النتائج
    results = []
    for opp in potential_opportunities:
        match_percent = calculate_match_score(student, opp)

        # نعرض فقط النتائج ذات المطابقة الجيدة (التي تمتلك مهارات كافية)
        if match_percent >= 25:
            results.append({
                'opportunity': opp,
                'score': round(match_percent, 1)
            })

    # ترتيب من الأعلى مطابقة إلى الأقل
    results.sort(key=lambda x: x['score'], reverse=True)

    return render(request, 'students/opportunities/matched_opportunities.html', {
        'student': student,
        'results': results,
        'count': len(results)
    })
# def match_opportunities(request):
#     print("MATCH_OPPORTUNITIES:")
#     # 1. جلب بروفايل الطالب المرتبط بالمستخدم الحالي بأمان
#     # إذا لم يكن للمستخدم بروفايل طالب، سيظهر خطأ 404 أو يمكن تحويله لإنشاء بروفايل
#     student = get_object_or_404(StudentProfile, user=request.user)
#
#     # 2. بناء استعلام ذكي لجلب الفرص المحتملة
#     # نجلب الفرص التي: (تطابق تخصص الطالب أو عامة) وَ (معدلها المطلوب أقل من معدل الطالب أو غير محدد)
#     query = Q()
#
#     # فلتر التخصص: الفرص التي تطابق تخصص الطالب أو الفرص التي تقبل الجميع (null)
#     if student.major:
#         query &= (Q(major=student.major) | Q(major__isnull=True))
#
#     # فلتر المعدل: استبعاد الفرص التي تطلب معدلاً أعلى من معدل الطالب الحالي
#     if student.gpa is not None:
#         query &= (Q(min_gpa__lte=student.gpa) | Q(min_gpa__isnull=True))
#
#     # جلب الفرص مع prefetch_related لتحسين الأداء عند قراءة المهارات داخل الحلقة
#     potential_opportunities = TrainingOpportunity.objects.filter(query).prefetch_related('required_skills').distinct()
#
#     def calculate_match_score(std, opp):
#         score = 0
#
#         # أ. فحص التخصص (40 درجة)
#         if std.major and opp.major and std.major == opp.major:
#             score += 40
#         elif not opp.major:  # فرص عامة تعطي نقاط أقل في معيار التخصص
#             score += 20
#
#         # ب. فحص المعدل (30 درجة)
#         try:
#             if std.gpa is not None and opp.min_gpa is not None:
#                 if std.gpa >= opp.min_gpa:
#                     score += 30
#                     # بونص للطالب المتفوق (5 درجات إضافية)
#                     if std.gpa >= (opp.min_gpa + Decimal('0.5')):
#                         score += 5
#             elif opp.min_gpa is None:  # إذا كانت الفرصة لا تشترط معدلاً
#                 score += 25
#         except (TypeError, InvalidOperation):
#             pass
#
#         # ج. فحص المهارات (30 درجة)
#         try:
#             if opp.required_skills.exists() and std.skills.exists():
#                 # تحويل المهارات إلى مجموعات (Sets) للمقارنة السريعة
#                 opp_skills = {str(s.name).lower() for s in opp.required_skills.all() if s.name}
#                 std_skills = {str(s.name).lower() for s in std.skills.all() if s.name}
#
#                 if opp_skills:
#                     matches = opp_skills.intersection(std_skills)
#                     # حساب النسبة المئوية للمهارات المتوفرة لدى الطالب من أصل مهارات الفرصة
#                     score += (len(matches) / len(opp_skills)) * 30
#         except AttributeError:
#             pass
#
#         return min(score, 100)
#
#     # 3. معالجة النتائج وترتيبها
#     results = []
#     for opp in potential_opportunities:
#         match_percent = calculate_match_score(student, opp)
#
#         # نعرض فقط الفرص التي تحقق حد أدنى من القبول (مثلاً 20%) لزيادة الخيارات
#         if match_percent >= 20:
#             results.append({
#                 'opportunity': opp,
#                 'score': round(match_percent, 1)
#             })
#
#     # ترتيب النتائج من الأعلى مطابقة إلى الأقل
#     results.sort(key=lambda x: x['score'], reverse=True)
#
#     return render(request, 'students/opportunities/matched_opportunities.html', {
#         'student': student,
#         'results': results,
#         'count': len(results)
#     })


