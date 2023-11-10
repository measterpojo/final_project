from core.context import DABContext
from core.utils import is_site_admin

from django.conf import settings

class CommentDABContext(DABContext):
    

    def get_comments(self):


        comments = self.model_object.comments.filter_parents_by_object(
            self.model_object, include_flagged = is_site_admin(self.request.user)
        )
        return comments
    
    
    def __call__(self):

        context = super(CommentDABContext, self).__call__()


        context.update({
            'comments': self.get_comments(),
            'allowed_flags': settings.COMMENT_FLAGS_ALLOWED,
            'is_anonymous_allowed': settings.COMMENT_ALLOW_ANONYMOUS,
            'is_subscription_allowed': settings.COMMENT_ALLOW_SUBSCRIPTION,
            'is_blocking_allowed': settings.COMMENT_ALLOW_BLOCKING_USERS,
            
            })


        return context
