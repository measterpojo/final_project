from django import template

from core.utils import is_site_admin


from core.messages import ReactionError

from reactions.models import ReactionInstance

from flags.models import FlagInstance
from flags.managers import FlagInstanceManager

from followers.models import Follower

from django.contrib.admin.options import get_content_type_for_model


register = template.Library()


@register.simple_tag(name='get_model_name')
def get_model_name(obj):
    """returns the model name of an object"""
    return type(obj).__name__


@register.simple_tag(name='get_app_name')
def get_app_name(obj):
    """returns the app name of an objects"""
    return type(obj)._meta.app_label



@register.simple_tag(name='render_field')
def render_field(field, **kwargs):
    field.field.widget.attrs.update(kwargs)
    return field


@register.simple_tag(name='can_delete')
def can_delete(obj, user):
    return is_site_admin(user) or obj.user == user




@register.simple_tag(name='has_reacted')
def has_reacted(obj, user, reaction):

    print(obj, 'obj')

    print(get_content_type_for_model(obj), 'get_content')

    """
    Returns whether a user has reacted with a particular reaction on a comment or not.
    """
    if user.is_authenticated:
        reaction_type = getattr(ReactionInstance.ReactionType, reaction.upper(), None)
        if not reaction_type:
            raise template.TemplateSyntaxError(ReactionError.TYPE_INVALID.format(reaction_type=reaction))
        return ReactionInstance.objects.filter(
            user=user,
            reaction_type=reaction_type.value,
            reaction__content_type=get_content_type_for_model(obj),
            reaction__object_id=obj.id,
            ).exists()

    return False


@register.simple_tag(name='render_flag_reasons')
def render_flag_reasons():
    return FlagInstanceManager.reason_list

# <------------ FILTER ------------------>
# follows
@register.filter(name='has_followed')
def has_followed(user, model_object):
    if user.is_authenticated:
        return 

# flags
@register.filter(name='has_flagged')
def has_flagged(user, obj):
    if user.is_authenticated:
        return FlagInstance.objects.filter(user=user, flag__content_object = obj)
    return False



