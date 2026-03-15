from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from academy.models import College, Major
from core.routes import Routes
from students.models import StudentProfile
from training_entities.decorators import training_entity_required
from training_entities.forms import TrainingEntityProfileForm, TrainingOpportunityForm
from training_entities.models import TrainingEntityProfile, TrainingOpportunity
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from decimal import Decimal, InvalidOperation


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
@training_entity_required
def opportunity_detail(request,id):

    profile = get_object_or_404(TrainingEntityProfile, user=request.user)
    opportunity = get_object_or_404(TrainingOpportunity, id=id, provider=profile)

    context = {
        'opportunity': opportunity,
    }
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

    def calculate_match_score(opp, std):
        score = 0

        # فحص التخصص بأمان
        if opp.major and std.major and std.major == opp.major:
            score += 40

        # فحص المعدل بأمان (الاحتياط الثاني: معالجة أنواع البيانات)
        try:
            if std.gpa is not None and opp.min_gpa is not None:
                if std.gpa >= opp.min_gpa:
                    score += 30
                    # بونص التفوق
                    if std.gpa > (opp.min_gpa + Decimal('0.5')):
                        score += 5
        except (TypeError, InvalidOperation):
            pass  # في حال فشل المقارنة الحسابية، نتجاوزها دون تعطيل الكود

        # فحص المهارات بأمان (الاحتياط الثالث: Many-to-Many)
        try:
            # نتحقق من وجود مهارات لدى الطرفين قبل البدء
            if opp.required_skills.exists() and std.skills.exists():
                opp_skills = set(opp.required_skills.values_list('name', flat=True))
                std_skills = set(std.skills.values_list('name', flat=True))

                # تنظيف النصوص (Lower case) وتجنب الأخطاء إذا كانت الأسماء None
                opp_skills = {str(s).lower() for s in opp_skills if s}
                std_skills = {str(s).lower() for s in std_skills if s}

                if opp_skills:
                    matches = opp_skills.intersection(std_skills)
                    score += (len(matches) / len(opp_skills)) * 30
        except AttributeError:
            pass  # في حال كانت العلاقة غير موجودة أصلاً

        return min(score, 100)

    # 3. معالجة النتائج
    results = []
    for student in potential_students:
        match_percent = calculate_match_score(opportunity, student)
        # الاحتياط الرابع: التأكد من وجود قيمة للسكور قبل الإضافة
        if match_percent and match_percent > 30:
            results.append({
                'student': student,
                'score': round(match_percent, 1)  # تقريب الرقم لشكل أفضل
            })

    # ترتيب النتائج بأمان
    results.sort(key=lambda x: x['score'], reverse=True)

    return render(request, f'training_entities/opportunities/matched_students.html', {
        'opportunity': opportunity,
        'results': results,
        'count': len(results)
    })

# def check_match(request, opportunity_id):
#     def calculate_match_score(opportunity, student):
#         score = 0
#
#         # 1. فحص التخصص (40 نقطة)
#         if student.major == opportunity.major:
#             score += 40
#
#         # 2. فحص المعدل التراكمي (30 نقطة)
#         # إذا كان معدل الطالب أعلى من أو يساوي الحد الأدنى المطلوب
#         if student.gpa and opportunity.min_gpa:
#             if student.gpa >= opportunity.min_gpa:
#                 score += 30
#                 # بونص إضافي: إذا كان الطالب متفوقاً جداً (أعلى من المطلوب بكثير)
#                 # تحويل Decimal إلى float قبل الجمع
#                 if float(student.gpa) > (float(opportunity.min_gpa) + 0.5):
#                     score += 5
#
#                     # 3. فحص المهارات (30 نقطة)
#         if opportunity.required_skills and student.skills:
#             # opp_skills = set(s.strip().lower() for s in opportunity.required_skills.split(','))
#             # std_skills = set(s.strip().lower() for s in student.skills.split(','))
#             # جلب المهارات المطلوبة من الفرصة (كأسماء)
#             opp_skills = set(opportunity.required_skills.values_list('name', flat=True))
#             opp_skills = {s.lower() for s in opp_skills}
#
#             # جلب مهارات الطالب (كأسماء)
#             std_skills = set(student.skills.values_list('name', flat=True))
#             std_skills = {s.lower() for s in std_skills}
#
#             matches = opp_skills.intersection(std_skills)
#             if opp_skills:
#                 score += (len(matches) / len(opp_skills)) * 30
#
#         return min(score, 100)  # التأكد أن النتيجة لا تتعدى 100
#
#
#     opportunity = get_object_or_404(TrainingOpportunity, id=opportunity_id)
#
#     # جلب الطلاب الذين لديهم على الأقل تخصص مطابق أو مهارة واحدة مشابهة
#     potential_students = StudentProfile.objects.filter(
#         Q(major=opportunity.major) |
#         Q(gpa__gte=opportunity.min_gpa)
#     ).distinct()
#
#     results = []
#     for student in potential_students:
#         match_percent = calculate_match_score(opportunity, student)
#         if match_percent > 30:  # عرض الطلاب الذين لديهم مطابقة أكثر من 30% فقط
#             results.append({
#                 'student': student,
#                 'score': match_percent
#             })
#
#     # ترتيب النتائج من الأعلى للأقل
#     results = sorted(results, key=lambda x: x['score'], reverse=True)
#
#     return render(request, f'{app_name}/opportunities/matched_opportunities.html', {
#         'opportunity': opportunity,
#         'results': results
#     })

# def training_opportunity2(request, id=None):
#     entity_profile = get_object_or_404(TrainingEntityProfile, user=request.user)
#
#     opportunity = None
#     if id:
#         opportunity = get_object_or_404(TrainingOpportunity, id=id, provider=entity_profile)
#
#     if request.method == "POST":
#         form = TrainingOpportunityForm(request.POST, request.FILES, instance=opportunity)
#         if form.is_valid():
#             # 1. حفظ البيانات الأساسية
#             new_opportunity = form.save(commit=False)
#             new_opportunity.provider = entity_profile
#             new_opportunity.save()
#
#             # 2. حفظ التخصص (Majors) - تأكد من وضع الكائن داخل مصفوفة [ ]
#             selected_major = form.cleaned_data.get('majors')
#             if selected_major:
#                 # العلاقة ManyToMany تتطلب iterable (مصفوفة)
#                 new_opportunity.majors.set([selected_major])
#
#             # 3. حفظ المهارات (Skills)
#             skills = form.cleaned_data.get('required_skills')
#             print(f"--- Debug: skills_text: {len(skills)} ---")
#             # if skills_text:
#             #     skill_names = [n.strip() for n in skills_text.split(',') if n.strip()]
#             #     skill_objects = []
#             #     for name in skill_names:
#             #         skill_obj, _ = Skill.objects.get_or_create(name=name)
#             #         skill_objects.append(skill_obj)
#             #
#             #     # ربط المهارات يدوياً
#             #     new_opportunity.required_skills.set(skill_objects)
#             #
#             # # 4. الحل الحاسم للخطأ:
#             # # بدلاً من form.save_m2m() التي تسبب الخطأ، سنقوم بحفظ الحقول الأخرى فقط (إن وجدت)
#             # # أو ببساطة تجاهلها لأننا حفظنا الـ ManyToMany يدوياً بالأعلى.
#             # # احذف سطر form.save_m2m() أو استبدله بـ:
#             # try:
#             #     # حفظ أي حقول ManyToMany أخرى لم نعالجها يدوياً
#             #     form.save_m2m()
#             # except TypeError:
#             #     # إذا حدث خطأ بسبب التخصصات التي حفظناها يدوياً، نتجاهله
#             #     pass
#             #
#             # return redirect(f'{app_name}:opportunities_list')
#     else:
#         form = TrainingOpportunityForm(instance=opportunity)
#
#     context = {
#         'form': form,
#         'is_edit': bool(id),
#         'opportunity': opportunity
#     }
#     return render(request, f'{app_name}/opportunities/opportunity_form.html', context)

#
# def training_opportunity(request):
#     # 1. جلب بروفايل الجهة
#     try:
#         entity_profile = TrainingEntityProfile.objects.get(user=request.user)
#     except TrainingEntityProfile.DoesNotExist:
#         return redirect(Routes.LOGIN)
#
#     # 2. منطق الحفظ (عند النقر على الزر فقط)
#     if request.method == "POST":
#         form = TrainingOpportunityForm(request.POST, request.FILES)
#         if form.is_valid():
#             opportunity = form.save(commit=False)
#             opportunity.provider = entity_profile  # ربط الفرصة بالجهة هنا
#             opportunity.save()  # هنا فقط يتم الإضافة لقاعدة البيانات
#             return redirect(Routes.TRAINING_ENTITY_DASHBOARD)
#
#     # 3. منطق العرض (عند فتح الصفحة لأول مرة)
#     else:
#         # ننشئ فورم فارغ تماماً بدون إنشاء أي سجل في قاعدة البيانات
#         form = TrainingOpportunityForm()
#
#     return render(request, f'{app_name}/opportunities/opportunity_form.html', {'form': form})




