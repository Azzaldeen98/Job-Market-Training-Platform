from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from applications.models import JoinTrainingOpportunity
from core.routes import Routes
from core.utils import calculate_match_score
from students.decorators import student_required
from students.forms import StudentProfileForm
from students.models import StudentProfile
from students.utils import student_match_opportunities
from training_entities.models import TrainingOpportunity

# Create your views here.
app_name="students"

@login_required
@student_required
def dashboard(request):

    try:

        student = get_object_or_404(StudentProfile, user=request.user)
        context = {
            "opportunities_count": 0,
            "apps_count":0,
            "matches_count": 0,
        }

        if student:

            context['accepted_apps_count'] = JoinTrainingOpportunity.objects.filter(
                student=student,
                status__in=['Accepted', 'on_training', 'completed']
            ).count()

            # 2. إجمالي طلبات الانضمام الواردة (تم تصحيح .cou إلى .filter)
            context['apps_count'] = JoinTrainingOpportunity.objects.filter(
                student=student
            ).count()

            matches = student_match_opportunities(request)
            matches_count=0 if not matches else len(matches)
            context['matches_count'] = matches_count

            matches_persent=0
            if matches_count :
                for  match in matches:
                    matches_persent += match['score']
                matches_persent = matches_persent / matches_count

            context['matches_persent'] = matches_persent
            context['complete_profile_persent'] = student.complete_profile_persent
            # print( "student.skills>>")
            # print( student.skills)

            # profile=StudentProfile.objects.filter(user=request.user).prefetch_related('skills').distinct()
            context['skills'] = student.skills.all()


            # 5. عدد الدعوات المرسلة (إذا كان لديك حالة باسم Invited)
            # context['invited_apps_count'] = JoinTrainingOpportunity.objects.filter(
            #     student=student,
            #     status='Invited'
            # ).count()

            # context['on_training_apps_count'] = JoinTrainingOpportunity.objects.filter(
            #     student=student,
            #     status='on_training'
            # ).count()

    except StudentProfile.DoesNotExist:
        messages.error(request, _("Please complete your profile first to view opportunities that match your specialization"))
        return redirect(Routes.STUDENT_COMPLETE_PROFILE)

    return render(request, f'{app_name}/dashboard.html',context)



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
def opportunities_invitations(request):

    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        # إذا لم يوجد ملف، نوجهه لصفحة إنشاء الملف مع رسالة تنبيه
        messages.error(request, _("Please complete your profile first to view opportunities that match your specialization"))
        return redirect(f'{app_name}:complete_profile')  # تأكد من اسم الـ URL الصحيح لديك


    app_opportunities=JoinTrainingOpportunity.objects.filter(student_id=student)
    results=[]
    for app in app_opportunities:
        if app.status == JoinTrainingOpportunity.Status.INVITED:
            match_percent = calculate_match_score(student, app.opportunity)
            results.append({
                'app': app,
                'status': app.status,
                'score': round(match_percent, 1)
            })


    return render(request, f'{app_name}/opportunities/opportunities_invites.html', {
        'student': student,
        'results': results,
        'total_apps': len(results)
    })




@login_required
@student_required
def match_opportunities(request):

    student = get_object_or_404(StudentProfile, user=request.user)
    results= student_match_opportunities(request)

    return render(request,
                  f'{app_name}/opportunities/matched_opportunities.html', {
                      'student': student,
                      'results': results,
                      'total_opportunities': len(results)
                  })

@login_required
@student_required
def my_opportunities_apps(request):

    apps=[]

    if request.user.is_authenticated and request.user.is_fully_active:
        student = request.user.profile

        if student :
            apps= JoinTrainingOpportunity.objects.filter(
                student=student,
                # ~Q(status=JoinTrainingOpportunity.Status.INVITED),
             )
        #     results = []
        #
        #     for app in apps:
        #     if app.status == JoinTrainingOpportunity.Status.INVITED:
        #         match_percent = calculate_match_score(student, app)
        #         results.append({
        #             'app': app,
        #             'status': app.status,
        #             'score': round(match_percent, 1)
        #         })
        #
        # return render(request, f'{app_name}/opportunities/opportunities_invites.html', {
        #     'student': student,
        #     'results': results,
        #     'count': len(results)
        # })

    return render(request, f'{app_name}/opportunities/my_opportunities_apps.html', {
        "student":student,
        # "total_apps":len(apps),
        "apps":apps
    })
@login_required
@student_required
def opportunity_apply(request,id):

    opportunity = get_object_or_404(TrainingOpportunity, id=id)
    student = request.user.profile

    if student:
        application = JoinTrainingOpportunity.objects.filter(
            student=student,
            opportunity=opportunity
        ).first()

        if not application:

            JoinTrainingOpportunity.objects.create(
                student=student,
                opportunity=opportunity,
                status=JoinTrainingOpportunity.Status.PENDING
            )
            messages.success(request, f" apply is successfully.")


            # if application.status == JoinTrainingOpportunity.Status.INVITED:
            #     messages.warning(request, "This student has already been apply.")
            #
            # else:
            #     application.status = JoinTrainingOpportunity.Status.INVITED
            #     application.save()
            #     messages.success(request, "Request status updated to 'Invited'.")



    return redirect(f'{app_name}:check_match', opportunity_id=opportunity.id)

@login_required
@student_required
def opportunity_detail(request,id):

    student = get_object_or_404(StudentProfile, user=request.user)
    opportunity = get_object_or_404(TrainingOpportunity, id=id)
    has_applied =False
    if(student and opportunity):
        has_applied=JoinTrainingOpportunity.objects.filter(student=student, opportunity=opportunity).exists()


    matching_result = calculate_match_score(student, opportunity)
    context = {
        'matching_result': matching_result,
        'opportunity': opportunity,
        'has_applied': has_applied,
    }
    return render(request, f'{app_name}/opportunities/opportunity_detail.html', context)




# def match_opportunities(request):
#     # 1. جلب بروفايل الطالب
#     student = get_object_or_404(StudentProfile, user=request.user)
#
#     # 2. الاستعلام الأولي (فلترة أساسية)
#     # نجلب الفرص التي تطابق التخصص أو الفرص العامة
#     query = Q(major=student.major) | Q(major__isnull=True)
#
#     # فلترة صارمة للمعدل: إذا كان هناك معدل مطلوب، يجب أن يكون معدل الطالب أعلى منه أو يساويه
#     if student.gpa is not None:
#         query &= (Q(min_gpa__lte=student.gpa) | Q(min_gpa__isnull=True))
#     else:
#         # إذا الطالب لم يدخل معدله، نظهر له فقط الفرص التي لا تشترط معدلاً
#         query &= Q(min_gpa__isnull=True)
#
#     potential_opportunities = TrainingOpportunity.objects.filter(query).prefetch_related('required_skills').distinct()
#
#     def calculate_match_score(std, opp):
#         score = 0
#
#         # --- [ أ. المهارات: الوزن الأكبر (60 درجة) ] ---
#         skill_weight = 60
#         try:
#             if opp.required_skills.exists() and std.skills.exists():
#                 opp_skills = {str(s.name).lower() for s in opp.required_skills.all() if s.name}
#                 std_skills = {str(s.name).lower() for s in std.skills.all() if s.name}
#
#                 if opp_skills:
#                     matches = opp_skills.intersection(std_skills)
#                     match_ratio = len(matches) / len(opp_skills)
#                     score += (match_ratio * skill_weight)
#
#                     # بونص للاتقان الكامل للمهارات
#                     if match_ratio == 1:
#                         score += 10
#         except Exception:
#             pass
#
#         # --- [ ب. التخصص: وزن متوسط (30 درجة) ] ---
#         if std.major and opp.major and std.major == opp.major:
#             score += 30
#         elif not opp.major:  # فرص عامة
#             score += 15
#
#         # --- [ ج. المعدل: ميزة إضافية (10 درجات) ] ---
#         # هنا المعدل لا يستبعد (لأن الاستبعاد تم في الكويري فوق)، بل يعطي بونص تميز
#         if opp.min_gpa is not None and std.gpa is not None:
#             if std.gpa >= opp.min_gpa:
#                 # بونص طردي: كلما زاد معدلك عن المطلوب زاد السكور قليلاً
#                 bonus = min(float(std.gpa - opp.min_gpa) * 5, 10)
#                 score += bonus
#
#         return min(score, 100)
#
#     # 3. بناء قائمة النتائج
#     results = []
#     for opp in potential_opportunities:
#         match_percent = calculate_match_score(student, opp)
#
#         # نعرض فقط النتائج ذات المطابقة الجيدة (التي تمتلك مهارات كافية)
#         if match_percent >= 25:
#             results.append({
#                 'opportunity': opp,
#                 'score': round(match_percent, 1)
#             })
#
#     # ترتيب من الأعلى مطابقة إلى الأقل
#     results.sort(key=lambda x: x['score'], reverse=True)
#
#     return render(request, f'{app_name}/opportunities/matched_opportunities.html', {
#         'student': student,
#         'results': results,
#         'count': len(results)
#     })




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


