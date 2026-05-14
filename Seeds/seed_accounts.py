# import os
# import django
# from django.contrib.auth.hashers import make_password
#
# from training_entities.models import TrainingEntityProfile
#
# # تهيئة بيئة دجانغو
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# django.setup()
#
# from django.contrib.auth import get_user_model
# from core.models import City
#
# User = get_user_model()
#
#
# def create_training_accounts():
#     # قائمة جهات التدريب المراد إنشاؤها
#     entities = [
#         {
#             "email": "hr@aramco.com",
#             "username": "aramco_training",
#             "password": "Test@123",
#
#         },
#         {
#             "email": "academy@sdaia.gov.sa",
#             "username": "sadaia_academy",
#             "password": "Test@123",
#
#         },
#         {
#             "email": "training@taifchamber.org.sa",
#             "username": "taif_chamber",
#             "password": "Test@123",
#
#         },
#         {
#             "email": "contact@tuwaiq.edu.sa",
#             "username": "tuwaiq_academy",
#             "password": "Test@123",
#
#         }
#     ]
#
#     print("🚀 Starting account creation...")
#
#     for data in entities:
#         # 1. إنشاء حساب المستخدم
#         user, created = User.objects.get_or_create(
#             email=data['email'],
#             defaults={
#                 'username': data['username'],
#                 'password': make_password(data['password']),  # تشفير كلمة المرور
#                 'is_active': True,
#             }
#         )
#
#         if not created:
#             print(f"⚠️ User {data['username']} already exists.")
#         else:
#             print(f"👤 User {data['username']} created successfully.")
#
#         # 2. جلب المدينة لربطها بالبروفايل
#         city_obj = City.objects.filter(name__icontains=data['city']).first()
#
#         # 3. إنشاء البروفايل المرتبط بالحساب
#         profile, p_created = TrainingEntityProfile.objects.update_or_create(
#             user=user,
#             defaults={
#                 'entity_name': data['name'],
#                 'registration_number': data['reg_num'],
#                 'city': city_obj,
#                 'entity_type': 'PRIVATE',  # أو النوع المناسب حسب EntityType.choices
#                 'is_available': True
#             }
#         )
#
#         if p_created:
#             print(f"🏢 Profile for {data['name']} linked successfully.")
#
#     print("✅ Operation completed!")
#
#
# if __name__ == '__main__':
#     create_training_accounts()