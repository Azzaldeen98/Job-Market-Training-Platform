import os
import sys
import django
from django.contrib.auth.hashers import make_password



# إعداد البيئة
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import City
from accounts.models import Role
from training_entities.models import TrainingEntityProfile



User = get_user_model()

def seed_training_entities():

    identity_obj, _ = Role.objects.get_or_create(
        code="training_entity",
        defaults={
            "name": "Training Entity",
            "description": "Organizations that provide training opportunities for users",
            "is_identity": True,
            "requires_approval": True,
            "view_in_register": True
        }
    )

    entities_data = [
        {
            "username": "aramco_training",
            "email": "training@aramco.com",
            "password": "Test@123",
            "entity_name": "مركز أرامكو للتدريب",
            "city": "الظهران",
            "type": "PRIVATE",
            "reg_num": "1010000001",
            "desc": "برامج تدريبية متقدمة في مجالات الهندسة والطاقة."
        },
        {
            "username": "sadaia_academy",
            "email": "academy@sdaia.gov.sa",
            "password": "Test@123",
            "entity_name": "أكاديمية سدايا",
            "city": "الرياض",
            "type": "GOVERNMENT",
            "reg_num": "2020000002",
            "desc": "المركز الوطني للذكاء الاصطناعي وعلوم البيانات."
        },
        {
            "username": "tuwaiq_academy",
            "email": "info@tuwaiq.edu.sa",
            "password": "Test@123",
            "entity_name": "أكاديمية طويق",
            "city": "الرياض",
            "type": "PRIVATE",
            "reg_num": "3030000003",
            "desc": "معسكرات تقنية احترافية في البرمجة والأمن السيبراني."
        },
        {
            "username": "taif_chamber",
            "email": "training@taifchamber.org.sa",
            "password": "Test@123",
            "entity_name": "مركز تدريب غرفة الطائف",
            "city": "الطائف",
            "type": "GOVERNMENT",
            "reg_num": "4040000004",
            "desc": "تطوير المهارات الإدارية والمهنية لقطاع الأعمال بالطائف."
        }
    ]

    print("🚀 Starting User Accounts & Training Profiles seeding...")

    for item in entities_data:
        # 1. إنشاء أو جلب المستخدم (User Auth)
        # نربط المستخدم بالـ identity لضمان عمل الـ Signal الخاص بالصلاحيات
        user, u_created = User.objects.get_or_create(
            username=item['username'],
            defaults={
                'email': item['email'],
                'password': make_password(item['password']),
                'identity': identity_obj,
                'is_active': True
            }
        )

        if u_created:
            print(f"👤 User Created: {item['username']}")
        else:
            # إذا كان المستخدم موجوداً، نحدث الهوية للتأكد
            user.identity = identity_obj
            user.save()
            print(f"👤 User Found: {item['username']}")

        # 2. جلب المدينة
        city_obj = City.objects.filter(name__icontains=item['city']).first()
        if not city_obj:
            print(f"⚠️ City '{item['city']}' not found. Using None for {item['entity_name']}.")


        profile, p_created = TrainingEntityProfile.objects.update_or_create(
            user=user,
            defaults={
                'entity_name': item['entity_name'],
                'city': city_obj,
                'entity_type': item['type'],
                'registration_number': item['reg_num'],
                'description': item['desc'],
                'is_available': True
            }
        )

        status = "Created" if p_created else "Updated"
        print(f"🏢 Profile {status}: {item['entity_name']}")

    print("✅ All Training Entities and Accounts are ready!")

if __name__ == '__main__':
    seed_training_entities()

