from core.utils import is_site_admin

from django.conf import settings


def _is_moderation_enabled():
    return settings.COMMENT_FLAGS_ALLOWED or settings.COMMENT_ALLOW_BLOCKING_USERS


def can_moderate_flagging(user):
    return bool(
        is_site_admin(user)
    )

def is_comment_moderator(user):
    if _is_moderation_enabled():
        return user.groups.filter(name="comment_moderator").exists() or user.has_perm(
            "comment.delete_flagged_comment"
        )
    return False