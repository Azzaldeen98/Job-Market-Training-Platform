import os
import sys
import django
from datetime import date, timedelta


# 1. إعداد البيئة
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


from academy.models import   Skill,Major
from core.models import City
from training_entities.models import TrainingEntityProfile, Industry, TrainingOpportunity


def get_skills_from_list(skill_names):
    """دالة لجلب كائنات المهارات من قاعدة البيانات بناءً على أسمائها"""
    return Skill.objects.filter(name__in=skill_names)


def seed_training_opportunities():
    print("🚀 جاري ربط الفرص التدريبية بالمهارات المخزنة...")

    # جلب البيانات الأساسية
    entities = {e.entity_name: e for e in TrainingEntityProfile.objects.all()}

    # التأكد من وجود المجالات (Industries)
    tech_industry, _ = Industry.objects.get_or_create(name="تقنية المعلومات")
    eng_industry, _ = Industry.objects.get_or_create(name="الهندسة")

    opportunities_data = [
        {
            "provider_name": "أكاديمية طويق",
            "title": "معسكر تطوير تطبيقات الويب (Django)",
            "description": "تدريب مكثف على بناء أنظمة الويب باستخدام إطار عمل ديجانغو.",
            "industry": tech_industry,
            "city_name": "الرياض",
            "major_name": "علوم الحاسب",
            "capacity": 20,
            "min_gpa": 3.5,
            "gpa_scale": 5,
            # نفترض أن هذه المهارات مخزنة مسبقاً في جدول Skill
            "skill_names": ["Python (Django/Flask)", "SQL", "Teamwork"],
            "benefits": "شهادة معتمدة + فرصة توظيف"
        },
        {
            "provider_name": "مركز أرامكو للتدريب",
            "title": "هندسة العمليات الميدانية",
            "description": "تدريب عملي في منشآت النفط والغاز.",
            "industry": eng_industry,
            "city_name": "الظهران",
            "major_name": "الهندسة الميكانيكية",
            "capacity": 10,
            "min_gpa": 3.0,
            "gpa_scale": 4,
            "skill_names": ["Business Analysis", "Problem Solving", "Leadership"],
            "benefits": "مكافأة شهرية + سكن"
        }
    ]

    for data in opportunities_data:
        # 1. جلب جهة التدريب
        provider = entities.get(data['provider_name'])
        if not provider:
            print(f"⚠️ لم يتم العثور على الجهة: {data['provider_name']}")
            continue

        # 2. جلب التخصص والمدينة
        city_obj = City.objects.filter(name__icontains=data['city_name']).first()
        major_obj = Major.objects.filter(name__icontains=data['major_name']).first()

        if not major_obj:
            print(f"⚠️ لم يتم العثور على التخصص: {data['major_name']}")
            continue

        # 3. إنشاء أو تحديث الفرصة
        opportunity, created = TrainingOpportunity.objects.update_or_create(
            provider=provider,
            title=data['title'],
            defaults={
                'description': data['description'],
                'field': data['industry'],
                'city': city_obj,
                'major': major_obj,
                'capacity': data['capacity'],
                'min_gpa': data['min_gpa'],
                'gpa_scale': data['gpa_scale'],
                'benefits': data['benefits'],
                'status': 'open',
                'start_date': date.today() + timedelta(days=20),
                'end_date': date.today() + timedelta(days=80),
                'deadline': date.today() + timedelta(days=10),
            }
        )

        # 4. ربط المهارات المخزنة فقط (Filter)
        existing_skills = get_skills_from_list(data['skill_names'])
        if existing_skills.exists():
            opportunity.required_skills.set(existing_skills)
            print(f"   ✅ تم ربط {existing_skills.count()} مهارات بـ {opportunity.title}")
        else:
            print(f"   ❓ لم يتم العثور على أي من المهارات المحددة لـ {opportunity.title} في قاعدة البيانات.")

        status = "إنشاء" if created else "تحديث"
        print(f"📌 {status}: {opportunity.title}")

    print("✅ تم الانتهاء من تغذية الفرص التدريبية.")


if __name__ == '__main__':
    seed_training_opportunities()