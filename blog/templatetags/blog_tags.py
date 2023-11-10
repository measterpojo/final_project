import logging

from django import template
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse

from blog.forms import ArticleForm


logger = logging.getLogger(__name__)


register = template.Library()


@register.simple_tag
def timeformat(data):
    try:
        data.strftime(settings.TIME_FORMAT)
    except Exception as e:
        logger.error(e)
        return ""
    

@register.simple_tag
def datetimeformat(data):
    try:
        return data.strftime(settings.DATE_TIME_FORMAT)
    except Exception as e:
        logger.error(e)
    return ""



@register.simple_tag
def query(qs, **kwargs):
    return qs.filter(**kwargs)


@register.inclusion_tag('blog/article_info.html')
def load_article_detail(request, article, isindex, user):
    return {
        'request': request,
        'article': article,
        'isindex': isindex,
        'user': user,

    }

