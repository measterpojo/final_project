import logging
from django.utils import timezone

from blog.forms import ArticleForm
from core.utils import cache
from .models import Category, Article

logger = logging.getLogger(__name__)



def processor(requests):
    key = 'processor'

    logger.info('set processor cache.')
    value = {
            'article_form': ArticleForm(request=requests),
            'nav_category_list': Category.objects.all(),
            'nav_pages': Article.objects.filter(
                type='p',
                status='p'
            ),
        }
    # cache.set(key, value, 60 * 60 * 10)
    return value