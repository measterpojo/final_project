from django.views.generic import FormView

from typing import Any, Dict
from .context import DABContext

from core.messages import EmailInfo

from django.conf import settings

class BaseView(FormView):


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = context.pop('form')
        context.update(DABContext(self.request))
        return context
    
    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()    
        kwargs['request'] = self.request
        return kwargs



class BaseCreateView(BaseView):
    email_service = None

    def _initialize_email_service(self, comment, request):
        # self.email_service = DABEmailService(comment, request)
        pass

    def _send_notification_to_followers(self, comment, request):
        pass

        # if settings.COMMENT_ALLOW_SUBSCRIPTION:
        #     self._initialize_email_service(comment, request)
        #     self.email_service.send_notification_to_followers()

    def perform_save(self, obj, request):
        obj.save()
        self._send_notification_to_followers(obj, request)
        obj.refresh_from_db()
        return obj
    
    def _handle_anonymous(self, obj, request, api=False):
        self._initialize_email_service(obj, request)
        # self.email_service.send_confirmation_request(api=api)
        self.anonymous = True
        self.msg = EmailInfo.CONFIRMATION_SENT

    def perform_create(self, obj, request, api=False):

        if settings.COMMENT_ALLOW_ANONYMOUS and not obj.user:
            self._handle_anonymous(obj, request, api)
        else:
            comment = self.perform_save(obj, request)
        return comment