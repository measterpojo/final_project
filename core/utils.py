import logging
import os
import random
import string
import uuid
from hashlib import sha256

import markdown
import requests

from django.core.cache import cache
from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)


def is_site_admin(user):
    return user.groups.filter(name='site_admin').exists() or user.is_staff

def get_model_obj(app_name, model_name, model_id):
    content_type =  ContentType.objects.get(app_label=app_name, model=model_name.lower())
    model_object = content_type.get_all_objects_for_this_type(id=model_id)
    return model_object

def get_request_data(request, item, api=False):
    value = request.GET.get(item) or request.POST.get(item)
    if not value and api:
        value = request.data.get(item)
    return value

def get_user_for_request(request):
    if request.user.is_authenticated:
        return request.user
    return None

def id_generator(prefix='', chars=string.ascii_lowercase, len_id=6, suffix=''):
    return prefix + ''.join(random.choice(chars) for _ in range(len_id)) + suffix


def get_wrapped_words_number():
    words_number = 0
    if settings.WRAP_CONTENT_WORDS is None:
        return words_number
    try:
        words_number = int(settings.WRAP_CONTENT_WORDS)
    except (ValueError, TypeError):
        raise ImproperlyConfigured('WRAP_CONTENT_WORDS_NOT_INT')
    return words_number

def get_profile_content_type():
    profile_app_name = getattr(settings, 'PROFILE_APP_NAME', None)
    profile_model_name = getattr(settings, 'PROFILE_MODEL_NAME', None)
    if not profile_app_name or not profile_model_name:
        return None
    try:
        content_type = ContentType.objects.get(
            app_label=profile_app_name,
            model=profile_model_name.lower()
        )
    except ContentType.DoesNotExist:
        return None
    return content_type

def has_valid_profile():
    if getattr(settings, 'COMMENT_USE_GRAVATAR'):
        return True
    content_type = get_profile_content_type()
    if not content_type:
        return False
    profile_model = content_type.model_class()
    fields = profile_model._metal.get_fields()
    for field in fields:
        if hasattr(field, "upload_to"):
            return True
    return False

# <-------------- CACHE ---------------->
def get_sha256(str):
    m = sha256(str.encode('utf-8'))
    return m.hexdigest()

def cache_decorator(expiration=3*60):
    def wrapper(func):
        def news(*args, **kwargs):
            try:
                view = args[0]
                key = view.get_cache_key()
            except:
                key = None
            if not key:
                unique_str = repr((func, args, kwargs))

                m = sha256(unique_str.encode('utf-8'))
                key = m.hexdigest()
            value = cache.get(key)
            if value is not None:

                if str(value) == '__default_cache_value__':
                    return None
                else:
                    return value
            else:
                logger.debug(
                    'cache_decorator set cache:%s key:%s' %
                    (func.__name__, key))
                value = func(*args, **kwargs)
                if value is None:
                    cache.set(key, '__default_cache_value', expiration)
                else:
                    cache.set(key, value, expiration)
                return value
        return news
    return wrapper


def expire_view_cache(path, servername, serverport, key_prefix=None):
    from django.http import HttpRequest
    from django.utils.cache import get_cache_key

    request = HttpRequest()
    request.META = {'SERVER_NAME': servername, 'SERVER_PORT': serverport}
    request.path = path

    key = get_cache_key(request, key_prefix=key_prefix, cache=cache)
    if key:
        logger.info('expire_view_cache:get key:{path}'.format(path=path))
        if cache.get(key):
            cache.delete(key)
        return True
    return False


def delete_view_cache(prefix, keys):
    from django.core.cache.utils import make_template_fragment_key
    key = make_template_fragment_key(prefix, keys)
    cache.delete(key)


class CommonMarkdown:
    @staticmethod
    def _convert_markdown(value):
        md = markdown.Markdown(
            extensions=[
                'extra',
                'codehilite',
                'toc',
                'tables',
            ]
        )
        body = md.convert(value)
        toc = md.toc 
        return body, toc


