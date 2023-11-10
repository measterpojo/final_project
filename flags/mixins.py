from core.mixins import BasePermission, ObjectLevelMixin
from django.conf import settings
from .utils import can_moderate_flagging

from core.messages import FlagError, ErrorMessage
import abc


class BaseFlagPermission(BasePermission):
    def has_permission(self, request):
        if not settings.COMMENT_FLAGS_ALLOWED:
            self.reason = FlagError.SYSTEM_NOT_ENABLED
            return False
        return super().has_permission(request)


class CanSetFlagMixin(BaseFlagPermission, ObjectLevelMixin, abc.ABC):
    def has_object_permission(self, request, obj):
        
        return obj.user != request.user
    

class CanUpdateFlagStateMixin(BaseFlagPermission, ObjectLevelMixin, abc.ABC):
    def has_permission(self, request):
        if not can_moderate_flagging(request.user):
            self.reason = ErrorMessage.NOT_AUTHORIZED
            return False
        return super().has_permission(request)

    def has_object_permission(self, request, obj):
        if not obj.is_flagged:
            self.reason = FlagError.NOT_FLAGGED_OBJECT
        return obj.is_flagged