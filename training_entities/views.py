from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from academy.models import College, Major ,University
from applications.models import JoinTrainingOpportunity
from applications.utils import change_application_status
from core.routes import Routes
from core.utils import calculate_match_score
from students.models import StudentProfile
from training_entities.decorators import training_entity_required
from training_entities.forms import TrainingEntityProfileForm, TrainingOpportunityForm
from training_entities.models import TrainingEntityProfile
from .models import TrainingOpportunity
import uuid
app_name="training_entities"

def load_universities(request):
    # city_id = request.GET.get('city')
    universities = University.objects.all().order_by('name')
    # return render(request, 'academy/partials/university_options.html', {'universities': universities})
    return JsonResponse(list(universities), safe=False)
def load_colleges(request):
    university_id = request.GET.get('university_id')
    colleges = College.objects.filter(university_id=university_id).values('id', 'name')
    return JsonResponse(list(colleges), safe=False)

def load_majors(request):
    college_id = request.GET.get('college_id')
    majors = Major.objects.filter(college_id=college_id).values('id', 'name')
    return JsonResponse(list(majors), safe=False)

@login_required
@training_entity_required
def dashboard(request):
    try:
        training_entity = request.user.profile

        context={
            "opportunities_count":0,
            # "active_opportunities_count":0,
            "incoming_apps_count":0,
            "accepted_apps_count":0,
            "rejected_apps_count":0,
            "invited_apps_count":0,
            "on_training_apps_count":0,
        }
        if training_entity:
            context['opportunities_count'] = TrainingOpportunity.objects.filter(
                provider=training_entity
            ).count()

            # 2. إجمالي طلبات الانضمام الواردة (تم تصحيح .cou إلى .filter)
            context['incoming_apps_count'] = JoinTrainingOpportunity.objects.filter(
                opportunity__provider=training_entity
            ).count()

            # 3. عدد المقبولين أو من هم قيد التدريب أو انتهوا
            context['accepted_apps_count'] = JoinTrainingOpportunity.objects.filter(
                opportunity__provider=training_entity,
                status__in=['Accepted', 'on_training', 'completed']
            ).count()

            # 4. عدد الطلبات المرفوضة
            context['rejected_apps_count'] = JoinTrainingOpportunity.objects.filter(
                opportunity__provider=training_entity,
                status='Rejected'
            ).count()

            # 5. عدد الدعوات المرسلة (إذا كان لديك حالة باسم Invited)
            context['invited_apps_count'] = JoinTrainingOpportunity.objects.filter(
                opportunity__provider=training_entity,
                status='Invited'
            ).count()

            context['on_training_apps_count'] = JoinTrainingOpportunity.objects.filter(
                opportunity__provider=training_entity,
                status='on_training'
            ).count()


        return render(request, f'{app_name}/dashboard.html',context)

    except TrainingEntityProfile.DoesNotExist:
        messages.error(request, _("Please complete your profile "))
        return redirect(f'{app_name}:complete_profile')





@login_required
@training_entity_required
def training_entity_complete_profile(request):
    # if not request.user.is_training_entity:
    #     return redirect(Routes.HOME)

    # توليد رقم عشوائي مؤقت يُستخدم فقط في حال الإنشاء (Create)
    temp_reg_number = f"TEMP-{uuid.uuid4().hex[:8].upper()}"

    profile, created = TrainingEntityProfile.objects.get_or_create(
        user=request.user,
        defaults={'registration_number': temp_reg_number}
    )

    if request.method == "POST":
        form = TrainingEntityProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(Routes.TRAINING_ENTITY_DASHBOARD)
    else:
        form = TrainingEntityProfileForm(instance=profile)

    return render(request, f'{app_name}/complete_profile.html', {'form': form})

@login_required
@training_entity_required
def opportunities_list(request):
    # if not request.user.is_training_entity or not request.user.profile.training_profile.is_available
    # جلب الفرص الخاصة بالجهة التدريبية المسجلة دخولها حالياً
    opportunities = TrainingOpportunity.objects.filter(provider=request.user.profile)
    return render(request, f'{app_name}/opportunities/opportunity_list.html', {'opportunities': opportunities})


@login_required
@training_entity_required
def delete_opportunity(request, id):
    # التأكد من أن المستخدم يملك بروفايل جهة تدريب
    profile = get_object_or_404(TrainingEntityProfile, user=request.user)

    # التأكد من أن الفرصة موجودة وتخص هذه الجهة (لحماية البيانات)
    opportunity = get_object_or_404(TrainingOpportunity, id=id, provider=profile)

    if request.method == "POST":
        opportunity.delete()
        # التوجه لصفحة عرض الفرص بعد الحذف
        return redirect(f'{app_name}:training_opportunities')

    # في حال محاولة الدخول عبر رابط GET (إجراء أمان)
    return redirect(f'{app_name}:training_opportunities')


@login_required
def student_profile(request):
    # student_id, match_persent
    # student_id=None
    application_status = JoinTrainingOpportunity.Status.DRAFT

    if request.method == "POST":
        match_score=request.POST.get('match_score')
        student_id=request.POST.get('student_id')
        opportunity_id=request.POST.get('opportunity_id')
        application_status=request.POST.get('application_status')
    else:
        student_id=request.GET.get('student_id')

    if student_id:
        student = get_object_or_404(StudentProfile, id=student_id)
        data=student.card_data


        return render(request, f'{app_name}/student_profile.html', {
            'match_score':match_score,
            'application_status':application_status,
            'card_data':data
        })

    messages.error(request, "لم يتم تحديد طالب لعرض ملفه الشخصي.")
    return redirect(f'{app_name}:check_match', opportunity_id=opportunity_id)
@login_required

def opportunity_detail(request, id):
    # 1. جلب الفرصة (متاحة للجميع للمشاهدة)
    opportunity = get_object_or_404(TrainingOpportunity, id=id)
    context = {'opportunity': opportunity}

    if request.user.is_authenticated:
    # 2. إذا كان المستخدم "جهة تدريب" (صاحب الفرصة)
        if request.user.is_training_entity:
            # نتحقق إذا كان هو صاحب هذه الفرصة تحديداً لرؤية إحصائيات المتقدمين
            if opportunity.provider == request.user.is_training_entity:
                context['is_owner'] = True
                # هنا يمكنك إضافة قائمة المتقدمين للشركة
                context['applicants'] = opportunity.applicants.all()

        # 3. إذا كان المستخدم "طالباً"
        elif request.user.is_student:
            from core.utils import calculate_match_score
            from applications.models import JoinTrainingOpportunity

            student = request.user.profile

            # حساب نسبة التطابق
            context['match_score'] = calculate_match_score(student, opportunity)

            # التحقق هل قدم مسبقاً
            context['has_applied'] = JoinTrainingOpportunity.objects.filter(
                student=student,
                opportunity=opportunity
            ).exists()

    return render(request, f'{app_name}/opportunities/opportunity_detail.html', context)

@login_required
@training_entity_required
def incoming_apps(request):

    apps=[]
    if request.user.is_authenticated and request.user.is_approved_entity:

        entity = request.user.profile

        # print(entity)
        apps = []
        if entity:
            apps = JoinTrainingOpportunity.objects.filter(
                opportunity__provider=entity
                # ~Q(status=JoinTrainingOpportunity.Status.INVITED),
                # opportunity=opportunity
            )
    # messages.success(request, f"{'Applications successful!e' }%")

    return render(request, f'{app_name}/incoming_apps.html', {
        "total_apps":len(apps),
        "apps":apps
    })
@login_required
@training_entity_required
def opportunity_apps(request, id):
    # 1. جلب الفرصة (متاحة للجميع للمشاهدة)

    apps=[]
    if request.user.is_authenticated and request.user.is_training_entity:
        # student = request.user.profile
        opportunity = get_object_or_404(TrainingOpportunity, id=id)
        apps= JoinTrainingOpportunity.objects.filter(
            # student=student,
            ~Q(status=JoinTrainingOpportunity.Status.INVITED),
            opportunity=opportunity
        )

    return render(request, f'{app_name}/opportunities/opportunities_apps.html', {
        "opportunity":opportunity,
        "apps":apps
    })

@login_required
@training_entity_required
def training_opportunity(request, id=None):
    # استخدام الخاصية profile التي قمت بتعريفها مسبقاً في CustomUser لضمان الدقة
    profile = request.user.profile
    opportunity = None

    if id:
        opportunity = get_object_or_404(TrainingOpportunity, id=id, provider=profile)

    if request.method == "POST":
        form = TrainingOpportunityForm(request.POST, request.FILES, instance=opportunity)
        if form.is_valid():
            # 1. إنشاء الكائن في الذاكرة دون الحفظ النهائي في قاعدة البيانات
            new_opportunity = form.save(commit=False)

            # 2. إسناد الجهة المزودة (البروفايل) يدوياً قبل الحفظ
            if not id:  # نقوم بالإسناد فقط في حالة الإضافة الجديدة
                new_opportunity.provider = profile

            # 3. الآن قم بالحفظ الفعلي
            new_opportunity.save()
            form.save_m2m()


            return redirect(f'{app_name}:training_opportunities')
    else:
        form = TrainingOpportunityForm(instance=opportunity)

    context = {
        'form': form,
        'is_edit': bool(id),
        'opportunity': f
    }
    return render(request, f'{app_name}/opportunities/opportunity_form.html', context)

@login_required
@training_entity_required
def check_match(request, opportunity_id):
    opportunity = get_object_or_404(TrainingOpportunity, id=opportunity_id)

    # تحويل حالة أحرف تخصص الفرصة إن وجد لتسهيل الفحص
    opp_major_str = str(opportunity.major.name).strip().lower() if opportunity.major and hasattr(opportunity.major,
                                                                                                 'name') else ""
    if not opp_major_str and opportunity.major:
        opp_major_str = str(opportunity.major).strip().lower()

    # 1. بناء استعلام ذكي لجلب الطلاب بناءً على التخصص فقط كمرحلة أولى
    if opportunity.major and opp_major_str != "all":
        # جلب الطلاب من نفس التخصص المطلوب صراحة
        student_query = Q(major=opportunity.major)
    else:
        # إذا كانت الفرصة لجميع التخصصات (All) أو حقل التخصص فارغ، نجلب جميع الطلاب النشطين
        student_query = Q()

    # جلب الطلاب مع تحسين الأداء (Optimization) لتفادي استعلامات قاعدة البيانات المتكررة
    potential_students = StudentProfile.objects.filter(student_query).select_related('major').prefetch_related(
        'skills').distinct()

    results = []
    for student in potential_students:

        # 2. التحقق من حالة التقديم السابقة إن وجدت
        application = JoinTrainingOpportunity.objects.filter(student=student, opportunity=opportunity).first()
        std_opp_status = application.status if application else None

        # 3. الفحص الأكاديمي العادل والذكي للمعدل بعد توحيد الميزان مئوياً (0% - 100%)
        try:
            if opportunity.min_gpa is not None and student.gpa is not None:
                std_scale = float(getattr(student, 'gpa_scale', None) or (5.0 if float(student.gpa) <= 5.0 else 100.0))
                opp_scale = float(
                    getattr(opportunity, 'gpa_scale', None) or (5.0 if float(opportunity.min_gpa) <= 5.0 else 100.0))

                # حماية وتأمين أنظمة مقياس الـ 4.0
                if float(student.gpa) <= 4.0 and getattr(student, 'gpa_scale', None) is None: std_scale = 4.0
                if float(opportunity.min_gpa) <= 4.0 and getattr(opportunity, 'gpa_scale',
                                                                 None) is None: opp_scale = 4.0

                student_percentage = (float(student.gpa) / std_scale) * 100.0
                opportunity_percentage = (float(opportunity.min_gpa) / opp_scale) * 100.0

                # إذا كان معدل الطالب مئوياً أقل من الحد الأدنى للشركة، يتم استبعاده فوراً لحفظ الشروط الأكاديمية
                if student_percentage < opportunity_percentage:
                    continue
        except (ValueError, TypeError, ZeroDivisionError):
            pass

        # 4. استدعاء الدالة الذكية لحساب سكور المطابقة الفعلي (المهارات + التخصص + حوافز المعدل)
        match_percent = calculate_match_score(student, opportunity)

        # 5. الفلترة على الحد الأدنى لنسبة المطابقة للعرض الفعلي (أكبر من 30%)
        if match_percent and match_percent > 30:
            results.append({
                'student': student,
                'status': std_opp_status,
                'score': round(match_percent, 1)
            })

    # ترتيب النتائج من الطالب الأعلى تطابقاً وسكوراً للأقل
    results.sort(key=lambda x: x['score'], reverse=True)

    return render(request, 'training_entities/opportunities/matched_students.html', {
        'opportunity': opportunity,
        'results': results,
        'count': len(results)
    })
# def check_match(request, opportunity_id):
#
#     opportunity = get_object_or_404(TrainingOpportunity, id=opportunity_id)
#     query = Q(major=opportunity.major) if opportunity.major else Q()
#     if opportunity.min_gpa is not None:
#         query |= Q(gpa__gte=opportunity.min_gpa)
#     potential_students = StudentProfile.objects.filter(query).distinct() if query else StudentProfile.objects.none()
#     results = []
#     for student in potential_students:
#         application = JoinTrainingOpportunity.objects.filter(student=student, opportunity=opportunity).first()
#         std_opp_status = None
#         if application:
#             std_opp_status = application.status
#         # if application and application.status  and  not is_opportunity_active  :
#         match_percent = calculate_match_score(student,opportunity)
#
#         if match_percent and match_percent > 30:
#             results.append({
#                 'student': student,
#                 'status': std_opp_status,
#                 'score': round(match_percent, 1)
#             })
#     # Sort results safely
#     results.sort(key=lambda x: x['score'], reverse=True)
#     return render(request, f'training_entities/opportunities/matched_students.html', {
#         'opportunity': opportunity,
#         'results': results,
#         'count': len(results)
#     })













@login_required
@training_entity_required
def send_invite(request, opportunity_id, student_id):

    # 1. جلب البيانات الأساسية
    opportunity = get_object_or_404(TrainingOpportunity, id=opportunity_id)
    student = get_object_or_404(StudentProfile, id=student_id)

    # 2. البحث عن أي سجل موجود مسبقاً لهذا الطالب مع هذه الفرصة
    application = JoinTrainingOpportunity.objects.filter(
        student=student,
        opportunity=opportunity
    ).first()

    # 3. التحقق الأمني (Logic Guard)
    if application:

        if application.status == JoinTrainingOpportunity.Status.INVITED:
            messages.warning(request, "This student has already been invited.")

        elif application.status not in [JoinTrainingOpportunity.Status.DRAFT]:
            messages.error(request,"This student cannot be invited because they have already applied or their status is active.")

        else:
            application.status = JoinTrainingOpportunity.Status.INVITED
            application.save()
            messages.success(request, "Request status updated to 'Invited'.")
    else:

        JoinTrainingOpportunity.objects.create(
            student=student,
            opportunity=opportunity,
            status=JoinTrainingOpportunity.Status.INVITED
        )
        messages.success(request, f"The invitation to {student.user.get_full_name()} was sent successfully.")



    return redirect(f'{app_name}:check_match', opportunity_id=opportunity.id)\


@login_required
@training_entity_required
def applicant_acceptance(request,app_id):
    change_application_status(request, app_id, JoinTrainingOpportunity.Status.ACCEPTED)
    return redirect(f'{app_name}:incoming_apps')

@login_required
@training_entity_required
def applicant_rejected(request,app_id):
    change_application_status(request, app_id, JoinTrainingOpportunity.Status.REJECTED)
    return redirect(f'{app_name}:incoming_apps')


@login_required
@training_entity_required
def applicant_on_training(request,app_id):
    change_application_status(request,
                              app_id,
                              JoinTrainingOpportunity.Status.ON_TRAINING,
                              JoinTrainingOpportunity.Status.ACCEPTED)

    return redirect(f'{app_name}:incoming_apps')

@login_required
@training_entity_required
def applicant_completed(request,app_id):
    change_application_status(request,
                              app_id,
                              JoinTrainingOpportunity.Status.COMPLETED,
                              JoinTrainingOpportunity.Status.ON_TRAINING)

    return redirect(f'{app_name}:incoming_apps')



@login_required

@training_entity_required
def cancel_invite(request, opportunity_id, student_id):

    # 1. جلب البيانات الأساسية
    opportunity = get_object_or_404(TrainingOpportunity, id=opportunity_id)
    student = get_object_or_404(StudentProfile, id=student_id)

    # 2. البحث عن أي سجل موجود مسبقاً لهذا الطالب مع هذه الفرصة
    application = JoinTrainingOpportunity.objects.filter(
        student=student,
        opportunity=opportunity
    ).first()

    # 3. التحقق الأمني (Logic Guard)
    if application:
        if application.status == JoinTrainingOpportunity.Status.INVITED:
            application.delete()

            messages.success(request, "This student's invitation has been cancelled.")


    return redirect(f'{app_name}:check_match', opportunity_id=opportunity.id)

