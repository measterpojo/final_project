from unittest.mock import patch

from django.conf import settings

from .base import BaseCommentFlagTest
from flags.models import Flag
from django.core.exceptions import ValidationError

# class FlagModelTest(BaseCommentFlagTest):

#     def test_flag_count(self):
#         comment = self.comment

#         self.assertEqual(comment.flag.get().flag_count, 0)

#         comment.flag.get().increase_count()
#         comment.refresh_from_db()

#         self.assertEqual(comment.flag.get().flag_count, 1)

#         comment.flag.get().decrease_count()
#         comment.refresh_from_db()

#         self.assertEqual(comment.flag.get().flag_count, 0)

#     def test_comment_author(self):
#         comment = self.comment

#         self.assertEqual(comment.user.id, comment.flag.get().comment_author.id)

#         def test_comment_author(self):
#             comment = self.comment
#             self.assertEqual(comment.user, comment.flag.comment_author)


# class ToggleFlaggedStateTest(BaseCommentFlagTest):
#     @classmethod
#     def setUpTestData(cls) -> None:
#         super().setUpTestData()
#         cls.comment = cls.create_comment(cls.content_object_1)
#         cls.flag = cls.comment.flag
#         cls.create_flag_instance(cls.user_1, cls.comment)
#         cls.create_flag_instance(cls.user_2, cls.comment)
#         cls.flag.get().refresh_from_db()
    
#     @patch.object(settings, 'COMMENT_FLAGS_ALLOWED', 0)

#     def test_flag_disabled_with_flag_count_greater_than_allowed_count(self):
#         self.flag.state = self.flag.get().UNFLAGGED
#         self.flag.get().save()
#         self.flag.get().refresh_from_db()


#         assert self.flag.get().flag_count > settings.COMMENT_FLAGS_ALLOWED
#         self.flag.get().toggle_flagged_state()

#         self.assertEqual(self.flag.get().state, self.flag.get().UNFLAGGED)


#     @patch.object(settings, 'COMMENT_FLAGS_ALLOWED', 1)
#     def test_when_flagging_is_enabled(self):
#         self.flag.get().toggle_flagged_state()

#         self.assertEqual(self.flag.get().state, self.flag.get().FLAGGED)


#     @patch.object(settings, 'COMMENT_FLAGS_ALLOWED', 10)
#     def test_with_large_allowed_flag_count(self):
#         self.assertEqual(self.flag.get().flag_count, 2)
#         self.flag.get().toggle_flagged_state()

#         self.assertEqual(self.flag.get().state, self.flag.get().UNFLAGGED)


#     @patch.object(settings, 'COMMENT_FLAGS_ALLOWED', 10)
#     def test_with_large_allowed_flag_count(self):
#         self.assertEqual(self.flag.get().flag_count, 2)
#         self.flag.get().toggle_flagged_state()

#         self.assertEqual(self.flag.get().state, self.flag.get().UNFLAGGED)


# class ToggleStateTest(BaseCommentFlagTest):
    
#     @classmethod
#     def setUpTestData(cls) -> None:
#         super().setUpTestData()
#         cls.flag = cls.create_comment(cls.content_object_1).flag

#     def test_unflagged_state(self):
#         # toggle states occurs between rejected and resolved only
#         self.assertRaises(ValidationError, self.flag.get().toggle_state, self.flag.get().FLAGGED, self.moderator)
    
#     def test_rejected_state(self):
#         self.flag.get().toggle_state(self.flag.get().REJECTED, self.moderator)

#         self.assertEqual(self.flag.get().state, self.flag.get().REJECTED)
#         self.assertEqual(self.flag.get().moderator, self.moderator)

#     def test_passing_same_state_twice(self):
#         # passing RESOLVED state value for the first time
#         self.flag.get().toggle_state(self.flag.get().RESOLVED, self.moderator)
#         self.assertEqual(self.flag.get().state, self.flag.get().RESOLVED)

#         # passing RESOLVED state value for the second time
#         self.flag.get().toggle_state(self.flag.get().RESOLVED, self.moderator)
#         # state reset to FLAGGED
#         self.assertEqual(self.flag.get().state, self.flag.get().FLAGGED)


# class GetVerboseStateTest(BaseCommentFlagTest):
#     @classmethod
#     def setUpTestData(cls) -> None:
#         super().setUpTestData()
#         cls.flag = cls.create_comment(cls.content_object_1).flag


#     @patch('flags.models.Flag.get_clean_state')
#     def test_valid_state(self, mocked_get_clean_state):
#         mocked_get_clean_state.return_value = self.flag.get().FLAGGED

#         self.assertEqual(
#             self.flag.get().get_verbose_state(self.flag.get().FLAGGED),
#             self.flag.get().STATES_CHOICES[self.flag.get().FLAGGED-1][1],
#         )

#     @patch('flags.models.Flag.get_clean_state')
#     def test_invalid_state(self, mocked_get_clean_state):
#         mocked_get_clean_state.return_value = 100

#         self.assertIsNone(self.flag.get().get_verbose_state(100))
    

# class GetCleanStateTest(BaseCommentFlagTest):
#     @classmethod
#     def setUpTestData(cls) -> None:
#         super().setUpTestData()
#         cls.flag = cls.create_comment(cls.content_object_1).flag
    
#     def test_valid_state(self):
#         state = self.flag.get().get_clean_state(self.flag.get().FLAGGED)

#         self.assertEqual(state, Flag.FLAGGED)
    
#     def test_invalid_int(self):
#         self.assertRaises(ValidationError, self.flag.get().get_clean_state, 100)

#     def test_non_integeral_value(self):
#         self.assertRaises(ValidationError, self.flag.get().get_clean_state, 'Not int')

#     def test_passing_none(self):
#         self.assertRaises(ValidationError, self.flag.get().get_clean_state, None)


# class IsFlagEnabledTest(BaseCommentFlagTest):
#     @classmethod
#     def setUpTestData(cls):
#         super().setUpTestData()
#         cls.flag = cls.create_comment(cls.content_object_1).flag

#     @patch.object(settings, 'COMMENT_FLAGS_ALLOWED', 1)
#     def test_when_enabled(self):
#         self.assertIs(True, self.flag.get().is_flag_enabled)

#     @patch.object(settings, 'COMMENT_FLAGS_ALLOWED', 0)
#     def test_when_disabled(self):
#         self.assertIs(False, self.flag.get().is_flag_enabled)