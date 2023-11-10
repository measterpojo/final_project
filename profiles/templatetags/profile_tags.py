from django import template

from profiles.utils import get_gravatar_img, get_profile_instance

register = template.Library()


# @register.simple_tag(name='get_profile_url')
# def get_profile_url(obj):
#     """ returns profile url of user """
#     if not obj.user:
#         return get_gravatar_img(obj.email)
#     profile = get_profile_instance(obj.user)
#     if profile:
#         return profile.get_absolute_url()
#     return get_gravatar_img(obj.email)


# @register.simple_tag(name='get_img_path')
# def get_img_path(obj):
#     """ returns url of profile image of a user """
#     profile = get_profile_instance(obj.user)
#     if not profile:
#         return get_gravatar_img(obj.email)
#     for field in profile.__class__._meta.get_fields():
#         if hasattr(field, 'upload_to'):
#             return field.value_from_object(profile).url
#     return get_gravatar_img(obj.email)
 