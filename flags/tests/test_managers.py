from unittest.mock import patch

from django.core.exceptions import ValidationError

from django.conf import settings
from flags.models import FlagInstance, Flag

from .base import BaseCommentFlagTest



# class FlagInstanceModelTest(BaseCommentFlagTest):
#     def test_create_flag(self):
#         data = self.flag_data
#         comment = self.comment
#         instance = self.create_flag_instance(self.user, comment, **data)

#         self.assertIsNotNone(instance)
#         comment.refresh_from_db()
#         self.assertEqual(comment.flag.get().flag_count, 1)


# class FLagInstanceManagerTest(BaseCommentFlagTest):
    
#     def test_clean_reason_for_invalid_value(self):
#         data = self.flag_data.copy()
#         data.update({'reason': -1})

#         self.assertRaises(ValidationError, self.set_flag, self.user, self.comment,**data)
    
#     def test_clean_reason_for_wrong_type(self):
#         data = self.flag_data.copy()
#         data.update({'reason':'abc'})

#         self.assertRaises(ValidationError, self.set_flag, self.user, self.comment, **data)

#     def test_clean_for_last_reason_without_info(self):
#         data = self.flag_data.copy()
#         data.update({'reason': FlagInstance.objects.reason_values[-1]})

#         self.assertRaises(ValidationError, self.set_flag, self.user, self.comment, **data)
    
#     def test_clean_ignores_info_for_all_reasons_except_last(self):
#         data = self.flag_data.copy()
#         info = 'Hi'
#         data['info'] = info
#         user = self.user
#         comment = self.comment
#         self.set_flag(user, comment, **data)
#         instance = FlagInstance.objects.get(user=user, flag=comment.flag.get())

#         self.assertIsNone(instance.info)
    
#     def test_set_flag_for_create(self):
#         self.assertTrue(self.set_flag(self.user, self.comment, **self.flag_data))

#     def test_set_flag_for_delete(self):
#         self.assertFalse(self.set_flag(self.user_2, self.comment_2))

#     def test_create_flag_twice(self):
#         self.assertTrue(self.set_flag(self.user, self.comment, **self.flag_data))

#         self.assertRaises(ValidationError, self.set_flag, self.user, self.comment, **self.flag_data)
    
#     def test_un_flag_non_existent_flag(self):
#         self.assertRaises(ValidationError, self.set_flag, self.user, self.comment)