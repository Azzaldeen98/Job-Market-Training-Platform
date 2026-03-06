def global_user_prefs(request):
    if request.user.is_authenticated:
        return {
            'is_dark_mode': request.user.is_dark_mode,
            'user_lang': request.user.language_preference,
            'user_avatar': request.user.profile_picture.url if request.user.profile_picture else None,
        }
    return {
        'is_dark_mode': False,
        'user_lang': 'ar',
        'user_avatar': None,
    }