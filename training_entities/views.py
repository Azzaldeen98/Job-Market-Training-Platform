from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from academy.models import College, Major
from applications.models import JoinTrainingOpportunity
from core.routes import Routes
from core.utils import calculate_match_score
from students.models import StudentProfile
from training_entities.decorators import training_entity_required
from training_entities.forms import TrainingEntityProfileForm, TrainingOpportunityForm
from training_entities.models import TrainingEntityProfile
from .models import TrainingOpportunity

app_name="training_entities"


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
# @training_entity_approval_required
def dashboard(request):
    return render(request, f'{app_name}/dashboard.html')


@login_required
@training_entity_required
def training_entity_complete_profile(request):

    # if not request.user.is_training_entity:
    #     return redirect(Routes.HOME)

    profile, created = TrainingEntityProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = TrainingEntityProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # التوجه لصفحة النجاح بعد الحفظ
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
# training_entities/views.py
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

            student = request.user.student_profile

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
def training_opportunity(request, id=None):

    profile = get_object_or_404(TrainingEntityProfile, user=request.user)
    opportunity = None
    if id:
        opportunity = get_object_or_404(TrainingOpportunity, id=id, provider=profile)
    # else:
    #     opportunity, created = TrainingOpportunity.objects.get_or_create(provider=profile)

    if request.method == "POST":
        form = TrainingOpportunityForm(request.POST, request.FILES, instance=opportunity)
        if form.is_valid():
            form.save()
            # التوجه لصفحة النجاح بعد الحفظ
            return redirect(f'{app_name}:training_opportunities')
    else:
        form = TrainingOpportunityForm(instance=opportunity)

    context = {
        'form': form,
        'is_edit': bool(id),
        'opportunity': opportunity
    }
    return render(request, f'{app_name}/opportunities/opportunity_form.html', context)


@login_required
@training_entity_required
def check_match(request, opportunity_id):
    # 1. جلب الفرصة بأمان
    opportunity = get_object_or_404(TrainingOpportunity, id=opportunity_id)

    # 2. بناء استعلام ذكي يتجاهل القيم الفارغة (الاحتياط الأول)
    query = Q(major=opportunity.major) if opportunity.major else Q()

    if opportunity.min_gpa is not None:
        query |= Q(gpa__gte=opportunity.min_gpa)

    # إذا كانت الفرصة فارغة تماماً من البيانات، نجلب قائمة فارغة بدلاً من خطأ
    potential_students = StudentProfile.objects.filter(query).distinct() if query else StudentProfile.objects.none()

    # is_opportunity_active = is_current_date_active(opportunity.start_date, opportunity.end_date)

    results = []
    for student in potential_students:

        application = JoinTrainingOpportunity.objects.filter(student=student, opportunity=opportunity).first()

        std_opp_status = None
        if application:
            std_opp_status = application.status

        # if application and application.status  and  not is_opportunity_active  :
        match_percent = calculate_match_score(student,opportunity)
        # الاحتياط الرابع: التأكد من وجود قيمة للسكور قبل الإضافة
        if match_percent and match_percent > 30:
            results.append({
                'student': student,
                'status': std_opp_status,
                'score': round(match_percent, 1)  # تقريب الرقم لشكل أفضل
            })

    # ترتيب النتائج بأمان
    results.sort(key=lambda x: x['score'], reverse=True)

    return render(request, f'training_entities/opportunities/matched_students.html', {
        'opportunity': opportunity,
        'results': results,
        'count': len(results)
    })

@login_required
@training_entity_required
def send_invitation(request, opportunity_id, student_id):
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
            messages.warning(request, "لقد تم إرسال دعوة لهذا الطالب مسبقاً.")
            return redirect(f'{app_name}:check_match', opportunity_id=opportunity.id)

        if application.status not in [JoinTrainingOpportunity.Status.DRAFT]:
            messages.error(request, "لا يمكن دعوة هذا الطالب لأنه قدم بالفعل أو حالته نشطة.")
            return redirect(f'{app_name}:check_match', opportunity_id=opportunity.id)

    # 4. التنفيذ: إذا لم يوجد سجل أو كان 'draft'، نقوم بالتحديث/الإنشاء
    if not application:
        # إنشاء سجل جديد بحالة دعوة
        JoinTrainingOpportunity.objects.create(
            student=student,
            opportunity=opportunity,
            status=JoinTrainingOpportunity.Status.INVITED
        )
        messages.success(request, f"تم إرسال الدعوة إلى {student.user.get_full_name()} بنجاح.")
    else:
        # تحديث السجل الموجود (من draft إلى invited)
        application.status = JoinTrainingOpportunity.Status.INVITED
        application.save()
        messages.success(request, "تم تحديث حالة الطلب إلى 'مدعو'.")

    return redirect(f'{app_name}:check_match', opportunity_id=opportunity.id)



