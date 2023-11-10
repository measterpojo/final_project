from time import sleep
from unittest.mock import patch


from django.utils import timezone

from django.conf import settings
from comments.models import Comment

from comments.tests.base import BaseCommentManagerTest

from flags.models import Flag, FlagInstance

class CommentModelTest(BaseCommentManagerTest):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.parent_comment = cls.create_comment(cls.content_object_1)
    
    def test_parent_comment_properties(self):
        comment = self.parent_comment


        self.assertIsNotNone(comment)
        self.assertEqual(str(comment), f'comment by {comment.user}: {comment.content[:20]}')
        self.assertEqual(repr(comment), f'comment by {comment.user}: {comment.content[:20]}')
        self.assertTrue(comment.is_parent)
        self.assertEqual(comment.replies().count(), 0)
        self.assertIsNotNone(comment.urlhash)
    
    def test_child_comment_properties(self):
        comment = self.create_comment(self.content_object_1, parent=self.parent_comment)

        self.assertIsNotNone(comment)
        self.assertEqual(str(comment), f'reply by {comment.user}: {comment.content[:20]}')
        self.assertEqual(repr(comment), f'reply by {comment.user}: {comment.content[:20]}')
        self.assertFalse(comment.is_parent)
        self.assertEqual(self.parent_comment.replies().count(), 1)
        self.assertIsNotNone(comment.urlhash)
    
    def test_is_edited(self):
        comment = self.create_comment(self.content_object_1)
        self.assertFalse(comment.is_edited)

        comment.content = 'updated'
        sleep(1)
        comment.save()

        self.assertTrue(comment.is_edited)

    def test_is_edited_for_anonymous_comment(self):
        comment = self.create_anonymous_comment(posted=timezone.now() - timezone.timedelta(days=1))

        self.assertFalse(comment.is_edited)
    
    @patch.object(settings, 'COMMENT_FLAGS_ALLOWED', 1)
    @patch.object(settings, 'COMMENT_SHOW_FLAGGED', False)
    def test_replies_method_without_any_flags(self):
        init_count = self.parent_comment_2.replies().count()
        reply = self.parent_comment_2.replies().first()


        self.create_flag_instance(self.user_1, reply)
        self.create_flag_instance(self.user_2, reply)

        self.assertEqual(self.parent_comment_2.replies(include_flagged=False).count(), init_count -1)

    @patch.object(settings, 'COMMENT_FLAGS_ALLOWED', 1)
    @patch.object(settings, 'COMMENT_SHOW_FLAGGED', False)
    def test_replies_method_with_flags(self):
        init_count = self.parent_comment_2.replies().count()
        reply = self.parent_comment_2.replies().first()

        self.create_flag_instance(self.user_1, reply)
        self.create_flag_instance(self.user_2, reply)

        # the comment is hidden, since it is flagged.
        self.assertEqual(self.parent_comment_2.replies().count(), init_count - 1)



    # CANT CHANGE THE FLAG STATUS -- GENERIC REALTIONS
    @patch('comments.models.hasattr')
    def test_is_flagged_property(self, mocked_hasattr):
        comment = self.create_comment(self.content_object_2)
        self.assertEqual(comment.flag.get().state, comment.flag.get().UNFLAGGED)

        self.assertFalse(comment.is_flagged)

        # comment.flag.state = comment.flag.get().FLAGGED
        # comment.save()
        # self.assertTrue(comment.is_flagged)

        with patch.object(settings, 'COMMENT_FLAGS_ALLOWED', 0):
            self.assertIs(False, comment.is_flagged)


    @patch('comments.models.hasattr')
    def test_has_flagged_state(self, mocked_hasattr):
        comment = self.create_comment(self.content_object_2)
        self.assertEqual(comment.flag.get().state, comment.flag.get().UNFLAGGED)
        self.assertFalse(comment.has_flagged_state)


        # comment.flag.get().state = comment.flag.get().FLAGGED
        # self.assertTrue(comment.has_flagged_state)
    

        mocked_hasattr.return_value = False
        self.assertFalse(comment.has_flagged_state)

    

    @patch('comments.models.hasattr')
    def test_has_rejected_state(self, mocked_hasattr):
        comment = self.create_comment(self.content_object_2)
        self.assertEqual(comment.flag.get().state, comment.flag.get().UNFLAGGED)
        self.assertFalse(comment.has_rejected_state)


        # self.assertTrue(comment.has_rejected_state)

        mocked_hasattr.return_value = False
        self.assertFalse(comment.has_rejected_state)

    # CANT CHANGE THE FLAG STATUS -- GENERIC REALTIONS

    