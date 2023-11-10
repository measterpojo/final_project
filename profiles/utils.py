from django.conf import settings

import hashlib

from django.contrib.contenttypes.models import ContentType

def is_gravatar_enabled(email):
    return getattr(settings, 'COMMENT_USE_GRAVATAR')

def get_gravatar_img(email):
    if not is_gravatar_enabled() or not email:
        return settings.DEFAULT_PROFILE_PIC_LOC
    hashed_email = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return f'https://www.gravatar.com/avatar/{hashed_email}'


def get_profile_content_type():
    profile_app_name = getattr(settings, 'PROFILE_APP_NAME', None)
    profile_model_name = getattr(settings, 'PROFILE_MODEL_NAME', None)
    if not profile_app_name or not profile_model_name:
        return None
    try:
        content_type = ContentType.objects.get(
            app_label = profile_app_name,
            model=profile_app_name.lower()
        )
    except ContentType.DoesNotExist:
        return None
    return content_type

def get_profile_instance(user):
    try:
        return getattr(user, settings.PROFILE_MODEL_NAME.lower(), None)
    except AttributeError:
        return None
    

def has_valid_profile():
    if getattr(settings, 'COMMENT_USE_GRAVATAR'):
        return True
    
    content_type = get_profile_content_type()
    if not content_type:
        return False
    profile_model = content_type.model_class()
    fields = profile_model._meta.get_fields()
    for field in fields:
        if hasattr(field, 'upload_to'):
            return True
    return False


