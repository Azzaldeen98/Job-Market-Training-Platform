import os
import sys
import django


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()



from academy.models import City, University, College, Major


def seed_academic_data():
    # 1. تعريف البيانات الهيكلية
    academic_data = {
        "جامعة الملك سعود": {
            "city": "الرياض",
            "type": "PUB",  # Public
            "colleges": {
                "كلية علوم الحاسب والمعلومات": ["علوم الحاسب", "نظم المعلومات", "هندسة البرمجيات"],
                "كلية الهندسة": ["الهندسة المدنية", "الهندسة الكهربائية", "الهندسة الميكانيكية"],
                "كلية إدارة الأعمال": ["المحاسبة", "المالية", "التسويق"]
            }
        },
        "جامعة الملك عبدالعزيز": {
            "city": "جدة",
            "type": "PUB",
            "colleges": {
                "كلية الهندسة": ["الهندسة الصناعية", "الهندسة الكيميائية"],
                "كلية الحاسبات وتقنية المعلومات": ["تقنية المعلومات", "الأمن السيبراني"],
                "كلية الاقتصاد والإدارة": ["الإدارة العامة", "إدارة الموارد البشرية"]
            }
        },
        "جامعة الملك فهد للبترول والمعادن": {
            "city": "الظهران",
            "type": "PUB",
            "colleges": {
                "كلية هندسة الحاسب والعلوم": ["علوم الحاسب والهندسة", "شبكات الحاسب"],
                "كلية الهندسة التطبيقية": ["هندسة البترول", "هندسة الطيران"]
            }
        },
        "جامعة الأمير سلطان": {
            "city": "الرياض",
            "type": "PRV",  # Private
            "colleges": {
                "كلية علوم الحاسب": ["نظم المعلومات الحاسوبية"],
                "كلية القانون": ["القانون التجاري"]
            }
        },
        "جامعة الطائف": {
            "city": "الطائف",
            "type": "PUB",
            "colleges": {
                "كلية الحاسبات وتقنية المعلومات": [
                    "علوم الحاسب",
                    "تقنية المعلومات",
                    "هندسة الحاسب"
                ],
                "كلية الهندسة": [
                    "الهندسة المدنية",
                    "الهندسة الكهربائية",
                    "الهندسة الميكانيكية"
                ],
                "كلية إدارة الأعمال": [
                    "المحاسبة",
                    "التسويق"
                ],
                "كلية الخرمة الجامعية": [
                    "علوم الحاسب",
                    "الرياضيات",
                    "المحاسبة"
                ],
            }
        },
    }

    print("🚀 Start feeding academic data...")

    for uni_name, uni_info in academic_data.items():
        # البحث عن المدينة (البحث بالاسم العربي أو الإنجليزي حسب ما خزنته سابقاً)
        city_name = uni_info['city']
        city_obj = City.objects.filter(name__icontains=city_name).first()

        if not city_obj:
            print(f"⚠️ Warning: City '{city_name}' not found. Skipping {uni_name}.")
            continue

        # 2. تحديث أو إنشاء الجامعة (اسم الجامعة فريد)
        university, created = University.objects.update_or_create(
            name=uni_name,
            defaults={
                'city': city_obj,
                'type': uni_info['type']
            }
        )

        status = "Created" if created else "Updated"
        print(f"🏢 {status} University: {uni_name}")

        for college_name, majors in uni_info['colleges'].items():
            # 3. جلب أو إنشاء الكلية
            college, _ = College.objects.get_or_create(
                name=college_name,
                university=university
            )

            for major_name in majors:
                # 4. جلب أو إنشاء التخصص
                Major.objects.get_or_create(
                    name=major_name,
                    college=college
                )

    print("✅ All academic records synced successfully!")


if __name__ == '__main__':
    seed_academic_data()
