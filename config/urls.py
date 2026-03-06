"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import redirect_by_role # استيراد دالة التوجيه

urlpatterns = [
    # رابط تغيير اللغة
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),

    # نظام المصادقة (Allauth)
    path('accounts/account/', include('allauth.urls')),

    # روابط تطبيق الحسابات المخصص
    path('accounts/', include('accounts.urls')),

    # === [AUTO_GENERATED_URLS_START] ===
    # محرك الأتمتة سيضيف روابط الأدوار هنا (مثل students, companies)
    # === [AUTO_GENERATED_URLS_END] ===

    # روابط تطبيق core (يجب أن يكون في الأسفل غالباً لأنه يحتوي على الصفحة الرئيسية)
    path('', include('core.urls')),

    path('students/', include('students.urls')),

    # أداة التحديث التلقائي للمتصفح أثناء التطوير
    path("__reload__/", include("django_browser_reload.urls")),
]

# إعدادات الملفات الساكنة والوسائط في وضع التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)