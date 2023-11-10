from django.views import View

from blocker.models import BlockedUser, BlockedUserHistory
from core.mixins import CanBlockUsersMixin
from core.responses import UTF8JsonResponse, DABResponseData
from core.messages import BlockUserError

from django.conf import settings

User = settings.AUTH_USER_MODEL

class BaseToggleBlockingView(DABResponseData):
    response_class = None
    
    def get_response_class(self):
        assert self.response_class is not None, (
                "'%s' should either include a `response_class` attribute, "
                "or override the `get_response_class()` method."
                % self.__class__.__name__
        )
        return self.response_class

    def post(self, request, *args, **kwargs):
        response_class = self.get_response_class()
        request_data = request.POST or getattr(request, 'data', {})
        user_id = request_data.get('obj_id', None) 
        try:
            user = User.objects.get(id=int(user_id))
        except (User.DoesNotExist, ValueError, TypeError):
            self.error = {
                'detail': BlockUserError.INVALID
            }
            self.status = 400
            return response_class(self.json(), status=self.status)