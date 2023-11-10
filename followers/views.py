from django.shortcuts import render

from django.views.generic.base import View

from .models import Follower
from core.responses import UTF8JsonResponse, DABResponseData
from core.validators import ContentTypeValidator, DABEmailValidator
from core.messages import FollowError

from core.mixins import CanSubscribeMixin


class BaseToggleFollowView(ContentTypeValidator, DABResponseData):
    response_class = None

    def get_response_class(self):
        assert self.response_class is not None, (
                "'%s' should either include a `response_class` attribute, "
                "or override the `get_response_class()` method."
                % self.__class__.__name__
        )
        return self.response_class

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', None)
        response_class = self.get_response_class()
        if email and not DABEmailValidator(email).is_valid():
            self.error = {
                'invalid_email': DABEmailValidator.message
            }
            self.status = 400

        user = request.user
        if user.email:
            email = user.email

        if not email:
            self.error = {
                'email_required': FollowError.EMAIL_REQUIRED.format(model_object=str(self.model_obj))
            }
            self.status = 400
            return response_class(self.json(), status=self.status)

        if not user.email:
            user.email = email
            user.save()
        
        username = user.username or email.aplit('@')[0]
        following = Follower.objects.toggle_follow(email=email, model_object=self.model_obj, username=username)
        self.data = {
            'following': following,
            'app_name': self.model_obj._meta.app_label,
            'model_name': self.model_obj.__class__.__name__,
            'model_id': self.model_obj.id,
            'model_object': str(self.model_obj)
        }
        return response_class(self.json())
    

class ToggleFollowView(CanSubscribeMixin, BaseToggleFollowView, View):
    response_class = UTF8JsonResponse