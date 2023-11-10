from .validators import CommentValidateMixin
from core.mixins import CanEditMixin, CanDeleteMixin



class CanEditCommentMixin(CanEditMixin, CommentValidateMixin):
    pass


class CanDeleteCommentMixin(CanDeleteMixin, CommentValidateMixin):
    pass

