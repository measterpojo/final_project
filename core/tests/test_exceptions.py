import sys

from unittest.mock import patch
from rest_framework import status



from core.exceptions import BadRequest
from django.test import TestCase
from core.messages import ExceptionError



class ExceptionTest(TestCase):
    _default_detail = ExceptionError.BAD_REQUEST

    def test_can_create_custom_without_params(self):
        exception = BadRequest()

        self.assertEqual(exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(exception.detail, self._default_detail)
    
    def test_create_custom_error_with_params(self):
        detail = 'not found'
        exception = BadRequest(detail=detail, status_code=404)

        self.assertEqual(exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(exception.detail, detail)
    
    def test_create_custom_error_without_drf_installed(self):
        with patch.dict(sys.modules, {'rest_framework.exceptions': None}):
            from importlib import reload
            reload(sys.modules['core.exceptions'])
            from core.exceptions import BadRequest
            exception = BadRequest()

        self.assertEqual(exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(exception.detail, self._default_detail)