import os

from config import settings


def get_url_view(view_name, args_list=None):
    from django.urls import reverse, NoReverseMatch
    try:
        return reverse(view_name, args=args_list)
    except NoReverseMatch:
        # إذا لم يجد الرابط، سيعيد رابطاً وهمياً يوضح لك المشكلة في المتصفح
        return f"/error-not-found-link-named-{view_name}/"

def get_identities_dashboards():
    dashboards = getattr(settings, 'ROLE_DASHBOARDS', {})
    return dashboards
def get_identities_apps():
    site_roles = getattr(settings, 'SITE_ROLES', [])
    identity_apps={}
    for identity in site_roles:
        if identity['code'] and identity['is_identity'] and identity['app_name']:
            code=identity['code']
            identity_apps[code]=identity['app_name']

    return identity_apps


def get_app_name(role_code):
    identities_roles = getattr(settings, 'SITE_ROLES', [])
    if identities_roles:
        for identity in identities_roles:
            if identity['code'] == role_code and identity['app_name']:
                return identity['app_name']
    return None

def app_is_exists(app_name):
    if not app_name:
        return  False

    app_path = os.path.join(settings.BASE_DIR, app_name)
    return os.path.exists(app_path)