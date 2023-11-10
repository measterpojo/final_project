from abc import ABCMeta, abstractmethod
from typing import Collection, Optional
from django.http import JsonResponse
from core.utils import get_request_data

from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.core.validators import EmailValidator

from .messages import ContentTypeError, ExceptionError, EmailError
from .exceptions import BadRequest

class BaseValidatorMixin:

    __metaclass__ = ABCMeta
    api = False
    error = None

    def dispatch(self, request, *args, **kwargs):
        if self.api:
            return super().dispatch(request, *args, **kwargs)
        try:
            self.validate(request)
        except BadRequest as e:
            return JsonResponse({'type': ExceptionError.ERROR_TYPE, 'detail': e.detail}, status=400)
        return super().dispatch(request, *args, **kwargs)

    @abstractmethod
    def validate(self, request):
        pass


class ContentTypeValidator(BaseValidatorMixin):
    model_obj = None

    def validate_app_name(self, app_name):
        if not app_name:
            self.error = ContentTypeError.APP_NAME_MISSING

        if not ContentType.objects.filter(app_label=app_name).exists():
            self.error = ContentTypeError.APP_NAME_INVALID.format(app_name=app_name)
            raise BadRequest(self.error)
        return app_name


    def validate_model_name(self, model_name):
        if not model_name:
            self.error = ContentTypeError.MODEL_NAME_MISSING
            raise BadRequest(self.error)
        return str(model_name).lower()


    def validate_content_type_object(self, app_name, model_name):
        try:
            ct_object = ContentType.objects.get(model=model_name, app_label=app_name)
        except ContentType.DoesNotExist:
            self.error = ContentTypeError.MODEL_NAME_INVALID.format(model_name=model_name)
            raise BadRequest(self.error)
        return ct_object

    def validate_model_id(self, model_id):
        if not model_id:
            self.error = ContentTypeError.MODEL_ID_MISSING
            raise BadRequest(self.error)
        try:
            model_id = int(model_id)
        except ValueError:
            self.error = ContentTypeError.ID_NOT_INTEGER.format(var_name='model', id=model_id)
            raise BadRequest(self.error)
        return model_id


    def validate_model_object(self, app_name, model_name, model_id):
        ct_object = self.validate_content_type_object(app_name, model_name)
        model_class = ct_object.model_class()
        model_query = model_class.objects.filter(id=model_id)
        if not model_query.exists() and model_query.count() != 1:
            self.error = ContentTypeError.MODEL_ID_INVALID.format(model_id=model_id, model_name=model_name)
            raise BadRequest(self.error)
        return model_query.first()

    def validate(self, request):
        super().validate(request)
        app_name = get_request_data(request, 'app_name', self.api)
        model_name = get_request_data(request, 'model_name', self.api)
        model_id = get_request_data(request, 'model_id', self.api)
        validated_app_name = self.validate_app_name(app_name)
        validated_model_name = self.validate_model_name(model_name)
        validated_model_id = self.validate_model_id(model_id)
        self.model_obj = self.validate_model_object(validated_app_name, validated_model_name, validated_model_id)


class DABEmailValidator(EmailValidator):
    def __init__(self, email):
        super().__init__(EmailError.EMAIL_INVALID)
        self.email = email
    
    def is_valid(self):
        try:
            self(self.email)
            return True
        except ValidationError:
            return False