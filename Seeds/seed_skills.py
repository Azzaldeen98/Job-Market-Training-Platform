import os
import sys
import django

# 1. إعداد المسارات (للتأكد من رؤية التطبيقات)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)

# 2. إعداد بيئة Django (يجب أن يتم قبل استيراد أي موديل)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') # تأكد من اسم مجلد الإعدادات لديك
django.setup()


from academy.models import Skill, SkillCategory


# from models import , SkillCategory  # استبدل اسم التطبيق هنا


def seed_skills():

    # هيكل البيانات: الفئة -> الأيقونة -> المهارات
    data = {
        "البرمجة والتطوير": {
            "icon": "terminal",
            "skills": ["Python (Django/Flask)", "JavaScript (React)", "Flutter", "SQL", "DevOps"]
        },
        "التصميم والإبداع": {
            "icon": "palette",
            "skills": ["UI/UX Design", "Photoshop", "Illustrator", "Video Editing", "Figma"]
        },
        "الأعمال والإدارة": {
            "icon": "briefcase",
            "skills": ["Project Management", "Business Analysis", "Accounting", "HR Management"]
        },
        "التسويق والمبيعات": {
            "icon": "trending-up",
            "skills": ["SEO", "Content Marketing", "Social Media", "Digital Ads"]
        },
        "المهارات الناعمة": {
            "icon": "users",
            "skills": ["Leadership", "Problem Solving", "Teamwork", "Public Speaking"]
        },
        "اللغات": {
            "icon": "languages",
            "skills": ["Business English", "Arabic Writing", "Translation"]
        }
    }

    for cat_name, info in data.items():
        # 1. إنشاء أو تحديث الفئة مع الأيقونة
        category, created = SkillCategory.objects.get_or_create(
            name=cat_name,
            defaults={'icon_name': info['icon']}
        )

        # تحديث الأيقونة إذا كانت الفئة موجودة مسبقاً بأيقونة مختلفة
        if not created and category.icon_name != info['icon']:
            category.icon_name = info['icon']
            category.save()

        # 2. إنشاء المهارات وربطها بالفئة
        for skill_name in info['skills']:
            Skill.objects.get_or_create(
                name=skill_name,
                category=category
            )

    print("✅ تم بنجاح تغذية بيانات الفئات، الأيقونات، والمهارات.")


if __name__ == '__main__':
    seed_skills()