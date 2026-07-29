import os
import sys
import django


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Country,Region, City


def seed_saudi_geo_data():
    # 1. إنشاء أو جلب الدولة
    saudi_arabia, _ = Country.objects.get_or_create(
        name="المملكة العربية السعودية",
        defaults={'code': 'KSA'}  # افترضنا وجود حقل code في موديل Country
    )

    # 2. بيانات المناطق (الاسم والرمز) والمدن التابعة لها
    # الرموز (code) هنا اختيارية أو يمكن استبدالها بالرموز الرسمية
    data = {
        "منطقة الرياض": {
            "code": "RUH",
            "cities": ["الرياض", "الخرج", "المجمعة", "الدرعية"]
        },
        "منطقة مكة المكرمة": {
            "code": "MKH",
            "cities": ["مكة المكرمة", "جدة", "الطائف", "رابغ"]
        },
        "المنطقة الشرقية": {
            "code": "EPR",
            "cities": ["الدمام", "الخبر", "الجبيل", "الأحساء", "حفر الباطن"]
        },
        "منطقة المدينة المنورة": {
            "code": "MED",
            "cities": ["المدينة المنورة", "ينبع", "العلا"]
        },
        "منطقة القصيم": {
            "code": "QAS",
            "cities": ["بريدة", "عنيزة", "الرس"]
        },
        "منطقة عسير": {
            "code": "ASR",
            "cities": ["أبها", "خميس مشيط", "بيشة"]
        },
        "منطقة تبوك": {
            "code": "TAB",
            "cities": ["تبوك", "أملج"]
        },
    }

    print("🚀 بدء عملية إدخال البيانات الجغرافية...")

    for reg_name, info in data.items():
        # إنشاء المنطقة المرتبطة بالدولة
        region, created = Region.objects.get_or_create(
            name=reg_name,
            country=saudi_arabia,
            defaults={'code': info['code']}
        )

        if created:
            print(f"📍 تم إنشاء المنطقة: {reg_name}")

        # إنشاء المدن المرتبطة بالمنطقة
        for city_name in info['cities']:
            City.objects.get_or_create(
                name=city_name,
                region=region
            )

    print("✅ تم تحديث بيانات المناطق والمدن بنجاح!")


# if __name__ == '__main__':
#     seed_saudi_geo_data()