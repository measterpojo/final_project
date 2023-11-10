from core.context import DABContext
from comments.forms import CommentForm
from comments.context import CommentDABContext

from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.core.exceptions import ImproperlyConfigured

from django.conf import settings

from django import template

from core.utils import get_wrapped_words_number,is_site_admin

register = template.Library()


@register.simple_tag(name='get_comment_replies')
def get_comment_replies(comment, user):
    return comment.replies()


@register.simple_tag(name='get_comments_count')
def get_comments_count(obj, user):
    return obj.comments.all_comments_by_object(obj, include_flagged=is_site_admin(user)).count()

@register.simple_tag(name='get_replies_count')
def get_replies_count(comment, user):
    return comment.replies(include_flagged=is_site_admin(user)).count()

def render_comments(request, obj, oauth=False):
    """
    retrievies list of comment related to a cetain and renders the appropriate template
    """
    context = CommentDABContext(request, model_object=obj)
    context.update({
        'comment_form' : CommentForm(request=request),
        'oauth':oauth,
        'request':request,
    })
    return context

register.inclusion_tag('comments/base.html')(render_comments)

# MARKDOWN -------------------------------

def _render_markdown(content):
    try:
        import markdown as md
    except ModuleNotFoundError:
        raise ImproperlyConfigured(
            'Comment App: Cannot render content in markdown format because markdown extension is not available.'
            'You can install it by visting https://pypi.org/p/markdown or by using the command '
            '"python -m pip install django-comments-dab[markdown]".'
        )
    else:
        return md.markdown(
            conditional_escape(content),
            extensions=settings.MARKDOWN_EXTENSIONS,
            extension_config=settings.MARKDOWN_EXTENSION_CONFIG
        )

def render_content(comment, number=None, **kwargs):
    markdown = kwargs.get('markdown', False)
    if markdown:
        if number:
            Warning.warn((
                    'The argument number is ignored when markdown is set to "True".'
                    'No wrapping will take place for markdown formatted content.'
            ),
            RuntimeWarning,
            
            )
        return {
            'text_1': mark_safe(_render_markdown(comment.content)),
            'text_2': '',
            'urlhash': comment.urlhash,
        }
    try:
        number = int(number)
    except (ValueError, TypeError):
        number = get_wrapped_words_number()

    content = conditional_escape(comment.content)
    content_words = content.split()
    if not number or len(content_words) <= number:
        text_1 = content
        text_2 = None
    else:
        text_1 = ' '.join(content_words[:number])
        text_2 = ' '.join(content_words[number:])

    return {
        'text_1': mark_safe(text_1),
        'text_2': mark_safe(text_2) if text_2 else None,
        'urlhash': comment.urlhash
    }


register.inclusion_tag('comments/content.html')(render_content)
