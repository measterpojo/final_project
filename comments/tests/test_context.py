from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Page

from django.conf import settings


from .base import BaseCommentUtilsTest
from comments.context import CommentDABContext
from core.context import DABContext
from core.messages import ErrorMessage

from blog.models import Article

class DABContextTest(BaseCommentUtilsTest):
    def setUp(self):
        super().setUp()
        

        

        self.data = {
            'model_object': self.post_1,
            'model_name': 'Article',
            'model_id': self.post_1.id,
            'app_name': 'blog',
            'user': self.post_1.author,
            'page': 10,
        }

        self.request = self.factory.post('comment/create/', data=self.data)
        self.request.user = self.post_1.author

    def test_initialized_object_is_dict(self):
        self.assertIsInstance(DABContext(self.request), dict)

    def test_model_object_exist_even_if_not_provided(self):
        self.assertEqual(DABContext(self.request).model_object.first(), self.post_1)

    # no login in self.data yet
    # ---------------------------
    # @patch.object(settings, 'LOGIN_URL', 'login/')
    # def test_get_login_fails_when_missing_in_settings(self):
    #     with self.assertRaises(ImproperlyConfigured) as e:
    #         DABContext(self.request)
    #     self.assertTrue(DABContext(self.request).get('login_url').startswith('/'))

    # @patch.object(settings, 'LOGIN_URL', 'profile/login/')
    # def test_get_login_url_prepend_slash(self):
    #     self.assertFalse(settings.LOGIN_URL.startswith('/'))
    #     self.assertTrue(DABContext(self.request).get('login_url').startswith('/'))

    # @patch.object(settings, 'LOGIN_URL', '/profile/login/')
    # def test_get_login_url_success(self):
    #     self.assertTrue(DABContext(self.request).get('login_url'), '/profile/login/')


    def test_context_object_is_callable(self):
        context = DABContext(self.request)
        self.assertTrue(callable(context))

    def test_calling_text_object_return_default_values(self):
        context = DABContext(self.request, extra_1='test-1')
        self.assertEqual(len(context), len(context.__call__()) +1 )
        self.assertEqual(len(context()), len(context.__call__()))