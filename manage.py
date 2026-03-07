#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
# import os
# import sys
#
#
# def main():
#     """Run administrative tasks."""
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)
#
#
# if __name__ == '__main__':
#     main()



import os
import sys
from pathlib import Path

def auto_setup_env():
    """وظيفة ذكية تنشئ ملف .env إذا لم يكن موجوداً قبل إقلاع ديجانجو"""
    base_dir = Path(__file__).resolve().parent
    env_path = base_dir / '.env'

    if not env_path.exists():
        try:
            # استيراد أداة توليد المفاتيح من ديجانجو
            from django.core.management.utils import get_random_secret_key
            secret_key = get_random_secret_key()

            # محتوى ملف البيئة الافتراضي
            content = (
                f"APP_NAME=Django App\n"
                f"SECRET_KEY={secret_key}\n"
                f"DEBUG=True\n"
                f"ALLOWED_HOSTS=127.0.0.1,localhost\n"
                f"EMAIL_HOST_USER=\n"
                f"EMAIL_HOST_PASSWORD=\n"
            )

            with open(env_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ [Auto-Setup]: Created .env file at {env_path}")
        except Exception as e:
            print(f"⚠️ [Warning]: Could not auto-generate .env: {e}")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    # --- إضافة منطق التجهيز التلقائي هنا ---
    auto_setup_env()
    # --------------------------------------

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

