from django.http import JsonResponse
from .messages import ErrorMessage , BlockUserError

from abc import abstractmethod, ABC

from blocker.models import BlockedUser
from core.utils import is_site_admin
from django.core.exceptions import ImproperlyConfigured
from comments.validators import CommentValidateMixin
from core.messages import FollowError
from django.conf import settings

from core.responses import UTF8JsonResponse

class BasePermission:

    status = 403
    reason = ErrorMessage.NOT_AUTHORIZED

    def has_permission(self, request):
        return True
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission(request):
            data = {'status': self.status, 'reason': self.reason}
            return UTF8JsonResponse(status=self.status, data=data)
        return super().dispatch(request, *args, **kwargs)
    

class UserPermission(BasePermission):

    reason = BlockUserError.NOT_PERMITTED

    def has_permission(self, request):
        return not BlockedUser.objects.is_user_blocked(request.user.id, request.POST.get('email'))

class BaseAuthPermission(UserPermission):
    def has_permission(self, request):
        if not request.user.is_authenticated:
            self.reason = ErrorMessage.LOGIN_REQUIRED
            return False
        return super().has_permission(request)


class CanSubscribeMixin(BaseAuthPermission):
    def has_permission(self, request):
        if not settings.COMMENT_ALLOW_SUBSCRIPTION:
            self.reason = FollowError.SYSTEM_NOT_ENABLED
            return False
        return super().has_permission(request)


class ObjectLevelMixin(BaseAuthPermission):
    @abstractmethod
    def get_object(self):
        raise ImproperlyConfigured(
            ErrorMessage.METHOD_NOT_IMPLEMENTED.format(class_name=self.__class__.__name__, method_name='get_object()')
        )
    
    def has_object_permission(self, request, obj):
        return True

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not self.has_object_permission(request, obj):
            self.reason = ErrorMessage.NOT_AUTHORIZED
            data = {'status': self.status, 'reason': self.reason}
            return UTF8JsonResponse(status=self.status, data=data)
        return super().dispatch(request, *args, **kwargs)
    

class CanEditMixin(ObjectLevelMixin,CommentValidateMixin, ABC):
    def has_object_permission(self, request, obj):
        return request.user == obj.user
    

class CanDeleteMixin(ObjectLevelMixin, ABC):
    def has_object_permission(self, request, obj):
        return bool(
            request.user == obj.user or
            is_site_admin(request.user) 
            # (obj.is_flagged and is_comment_moderator(request.user))
        )

class CanBlockUsersMixin(BaseAuthPermission):
    reason = ErrorMessage.NOT_AUTHORIZED
    
    def has_permission(self, request):
        return  is_site_admin(request.user)


# _handle_anonymous and notifications
class CreateMixin:
    email_service = None

    def _handle_anonymous(self, obj, request, api=False):
        self.anonymouse = True
    
    def perform_create(self, obj, request, api=False):
        pass