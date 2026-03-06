# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction


# ملاحظة: نستخدم 'accounts.CustomUser' كنص بدلاً من استيراد الموديل مباشرة
# لتجنب الـ Circular Import Error
@receiver(post_save, sender='accounts.CustomUser')
def handle_user_identity_flow(sender, instance, created, **kwargs):
    """
    يعمل فور حفظ المستخدم. تم تأمينها ضد أخطاء الاستيراد والتعليق.
    """
    # 1. التحقق من وجود الهوية
    if instance.identity:

        # استيراد الدالة من ملف utils عند الحاجة فقط (Lazy Import)
        from .utils import create_dynamic_profile

        # 2. إنشاء البروفايل إذا لم يكن موجوداً
        if not instance.profile_id:
            # نستخدم transaction.on_commit لضمان أن البروفايل يُنشأ
            # فقط بعد نجاح حفظ المستخدم نهائياً في قاعدة البيانات
            transaction.on_commit(lambda: create_dynamic_profile(instance, instance.identity.code))

        # 3. مزامنة الصلاحيات
        if instance.identity.permissions.exists():
            # نستخدم .set() أو .add()، ولكن .add() مناسبة هنا
            instance.user_permissions.add(*instance.identity.permissions.all())


# @receiver(post_save, sender=CustomUser)
# def handle_user_activation(sender, instance, created, **kwargs):
#     if created:
#         # 1. إنشاء البروفايل تلقائياً
#         profile = Profile.objects.create(user=instance)
#
#         # 2. فحص أدوار المستخدم
#         # إذا كان المستخدم لا يملك أي دور يتطلب موافقة، نفعله فوراً
#         roles_needing_approval = instance.roles.filter(requires_approval=True)
#
#         if not roles_needing_approval.exists():
#             profile.is_verified = True
#             profile.save()
#
#
# # signals.py
# @receiver(m2m_changed, sender=CustomUser.roles.through)
# def sync_permissions_and_profiles(sender, instance, action, pk_set, **kwargs):
#     """
#     عند إضافة دور للمستخدم:
#     1. ننسخ كافة صلاحيات هذا الدور إلى حقل user_permissions الخاص بالمستخدم.
#     2. إذا كان الدور 'هوية'، ننشئ له البروفايل الخاص به.
#     """
#     if action == "post_add":
#         roles = Role.objects.filter(pk__in=pk_set)
#
#         for role in roles:
#             # ضخ الصلاحيات من الدور إلى المستخدم مباشرة
#             if role.permissions.exists():
#                 instance.user_permissions.add(*role.permissions.all())
#
#             # معالجة إنشاء البروفايل (فقط للهوية الأولى المضافة)
#             if role.is_identity and not instance.profile:
#                 # منطق المصنع الديناميكي (StudentProfile, etc.)
#                 create_dynamic_profile(instance, role.code)
#
# @receiver(post_save, sender=CustomUser)
# def handle_user_specific_profile(sender, instance, created, **kwargs):
#     """
#     بمجرد إنشاء المستخدم، نتحقق من دوره وننشئ له السجل في الجدول الصحيح
#     ثم نربطه عبر المفتاح الأجنبي العام (Generic FK).
#     """
#     if created:
#         specific_profile = None
#
#         # المنطق: افحص الدور وأنشئ السجل المناسب
#         if instance.has_role('student'):
#             specific_profile = StudentProfile.objects.create()
#         elif instance.has_role('company'):
#             specific_profile = CompanyProfile.objects.create()
#
#         # إذا تم إنشاء بروفايل نوعي، اربطه بكائن المستخدم
#         if specific_profile:
#             instance.profile_content_type = ContentType.objects.get_for_model(specific_profile)
#             instance.profile_object_id = specific_profile.id
#
#             # إذا كان الدور لا يتطلب موافقة، نجعل البروفايل موثقاً تلقائياً
#             if not instance.roles.filter(requires_approval=True).exists():
#                 specific_profile.is_verified = True
#                 specific_profile.save()
#
#             instance.save()