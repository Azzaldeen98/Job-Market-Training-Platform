import logging
from django.apps import apps
from django.db import transaction, DatabaseError
from django.contrib.contenttypes.models import ContentType
from .models import CustomUser
from django.conf import settings


logger = logging.getLogger(__name__)


def sync_roles_from_settings(sender, **kwargs):
    """
    مزامنة كاملة: تحديث، إضافة، وحذف الأدوار بناءً على الإعدادات.
    """
    from .models import Role

    # 1. جلب قائمة الأدوار من الإعدادات
    roles_list = getattr(settings, 'SITE_ROLES', [])

    if not roles_list:
        # إذا كانت القائمة فارغة تماماً، قد يكون من الخطر حذف كل شيء
        # لذا نكتفي بالخروج أو يمكنك اختيار حذف الكل إذا أردت.
        return

    # 2. استخراج جميع الأكواد (codes) الحالية في الإعدادات
    current_codes = [role.get('code') for role in roles_list if role.get('code')]

    # 3. تحديث أو إنشاء الأدوار الموجودة في القائمة
    for role_data in roles_list:
        Role.objects.update_or_create(
            code=role_data.get('code'),
            defaults={
                'name': role_data.get('name'),
                'is_identity': role_data.get('is_identity', True),
                'requires_approval': role_data.get('requires_approval', False),
                'view_in_register': role_data.get('view_in_register', True),
            }
        )

    # 4. الحذف الذكي: حذف أي دور في قاعدة البيانات "غير موجود" في الإعدادات
    deleted_count, _ = Role.objects.exclude(code__in=current_codes).delete()

    if deleted_count > 0:
        print(f"🗑️ Cleaned up {deleted_count} roles not present in settings.")

# def sync_roles_from_settings(sender, **kwargs):
#     """دالة احترافية لمزامنة الأدوار من الإعدادات إلى قاعدة البيانات"""
#     from .models import Role
#     roles_list = getattr(settings, 'SITE_ROLES', [])
#
#     for role_data in roles_list:
#         Role.objects.update_or_create(
#             code=role_data.get('code'),
#             defaults={
#                 'name': role_data.get('name'),
#                 'is_identity': role_data.get('is_identity', True),
#                 'requires_approval': role_data.get('requires_approval', False),
#                 'view_in_register': role_data.get('view_in_register', True),
#             }
#         )
#


def create_dynamic_profile(user_instance, role_code):
    """
    محرك إنشاء البروفايلات الديناميكي المخصص لعلاقة ForeignKey.
    """
    # 1. منع التكرار (Idempotency)
    if user_instance.profile_id:
        return None

    # 2. اكتشاف الموديل برمجياً (مثلاً: 'student' -> 'StudentProfile')
    model_name = f"{role_code.strip().title()}Profile".replace(" ", "")

    TargetModel = None
    for model in apps.get_models():
        if model.__name__ == model_name:
            TargetModel = model
            break

    if not TargetModel:
        logger.error(f"CRITICAL: الموديل {model_name} غير موجود. تأكد من إنشائه في models.py")
        return None

    try:
        with transaction.atomic():
            # 3. إنشاء سجل البروفايل في الجدول المخصص
            new_profile = TargetModel.objects.create()

            # 4. جلب الـ ContentType للربط
            content_type = ContentType.objects.get_for_model(TargetModel)

            # 5. التحديث الصامت لقاعدة البيانات (Silent Database Update)
            # نستخدم update لمنع إعادة تشغيل سجنل post_save (الحماية من اللوب)
            updated = CustomUser.objects.filter(pk=user_instance.pk, profile_id__isnull=True).update(
                profile_type=content_type,
                profile_id=new_profile.id
            )

            if updated:
                # تحديث الكائن في الذاكرة (Memory) للاستخدام الفوري
                user_instance.profile_type = content_type
                user_instance.profile_id = new_profile.id
                logger.info(f"SUCCESS: تم إنشاء وربط {model_name} للمستخدم {user_instance.username}")
                return new_profile

    except Exception as e:
        logger.error(f"ERROR: فشل إنشاء البروفايل الديناميكي: {str(e)}")
        return None