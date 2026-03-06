
import os
import re
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command


class Command(BaseCommand):
    help = 'أتمتة إنشاء تطبيقات الهوية بناءً على SITE_ROLES'

    def handle(self, *args, **options):
        roles = getattr(settings, 'SITE_ROLES', [])
        identity_codes = [r['code'] for r in roles if r.get('is_identity')]

        # المسار الصحيح لملف الروابط الرئيسي
        main_urls_path = os.path.join(settings.BASE_DIR, 'config', '../../urls.py')

        for code in identity_codes:
            # تحسين الجمع اللغوي: company -> companies
            if code.endswith('y'):
                app_name = f"{code[:-1]}ies"
            else:
                app_name = f"{code}s"

            if not os.path.exists(app_name):
                self.stdout.write(self.style.SUCCESS(f'🏗️  جارٍ إنشاء تطبيق لـ {code}: {app_name}'))

                # إنشاء التطبيق
                call_command('startapp', app_name)

                # تهيئة الملفات (Views, URLs, Templates)
                self._setup_app_content(app_name)

                # الحقن في urls.py
                self._inject_url_include(main_urls_path, app_name)
            else:
                self.stdout.write(self.style.WARNING(f'📍 التطبيق "{app_name}" موجود بالفعل.'))

    def _setup_app_content(self, app_name):
        # 1. القوالب
        template_path = os.path.join(app_name, 'templates', app_name)
        os.makedirs(template_path, exist_ok=True)
        with open(os.path.join(template_path, 'dashboard.html'), 'w', encoding='utf-8') as f:
            f.write("{% extends 'base.html' %}\n{% block content %}\n")
            f.write(f"<h1 class='text-2xl font-bold p-6'>Welcome to {app_name.capitalize()} Dashboard</h1>\n")
            f.write("{% endblock %}")

        # 2. ملف الروابط الداخلي
        with open(os.path.join(app_name, '../../urls.py'), 'w', encoding='utf-8') as f:
            f.write(f"from django.urls import path\nfrom . import views\n\napp_name = '{app_name}'\n\n")
            f.write("urlpatterns = [\n    path('dashboard/', views.dashboard, name='dashboard'),\n]")

        # 3. ملف الـ Views
        with open(os.path.join(app_name, 'views.py'), 'w', encoding='utf-8') as f:
            f.write(
                "from django.shortcuts import render\nfrom django.contrib.auth.decorators import login_required\n\n")
            f.write(
                f"@login_required\ndef dashboard(request):\n    return render(request, '{app_name}/dashboard.html')")

    def _inject_url_include(self, urls_path, app_name):
        with open(urls_path, 'r', encoding='utf-8') as f:
            content = f.read()

        line_to_add = f"    path('{app_name}/', include('{app_name}.urls')),"
        if line_to_add not in content:
            # البحث عن قائمة urlpatterns وحقن السطر
            new_content = re.sub(r'(urlpatterns = \[.*?)\n\]', rf'\1\n{line_to_add}\n]', content, flags=re.DOTALL)
            with open(urls_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            self.stdout.write(self.style.SUCCESS(f'🔗 تم ربط {app_name} بالمسار الرئيسي.'))