from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # 1. استيراد السجنلز العادية (مثل إنشاء البروفايل تلقائياً)
        import accounts.signals

        # 2. ربط سجنل المزامنة لتحديث الأدوار من الإعدادات
        from .utils import sync_roles_from_settings
        post_migrate.connect(sync_roles_from_settings, sender=self)

        print("✅ Accounts signals & Roles sync loaded successfully!")