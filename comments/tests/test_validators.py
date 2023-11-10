from django.http import JsonResponse
from django.test import TestCase
from django.views import View

from rest_framework import status

from .base import BaseCommentTest
from core.validators import BadRequest, BaseValidatorMixin
from core.messages import ExceptionError, ContentTypeError


class MackedContentTypeValidatorView(BaseValidatorMixin, View):
    api = False


class CustomValidationTest(TestCase):

    def test_without_param(self):
        validator = BadRequest()

        self.assertEqual(validator.status_code, status.HTTP_400_BAD_REQUEST)