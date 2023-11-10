from .base import BaseCommentManagerTest

from comments.models import Comment

from django.conf import settings

from unittest.mock import patch

class CommentModelManagerTest(BaseCommentManagerTest):

    def test_retrieve_all_parent_comments(self):

        all_comments = Comment.objects.all().count()
        self.assertEqual(all_comments, 10)

        parents_comments = Comment.objects.all_parents().count()
        self.assertEqual(parents_comments, 5)
    

    @patch.object(settings, 'COMMENT_FLAGS_ALLOWED', 1)
    def test_filtering_flagged_comment(self):
        comment = self.parent_comment_1
        self.assertEqual(Comment.objects.all_exclude_flagged().count(), self.increment)
        self.create_flag_instance(self.user_1, comment)
        self.create_flag_instance(self.user_2, comment)

        with patch.object(settings, 'COMMENT_SHOW_FLAGGED', False):
            self.assertEqual(Comment.objects.all_exclude_flagged().count(), self.increment - 1)

        with patch.object(settings, 'COMMENT_SHOW_FLAGGED', True):
            self.assertEqual(Comment.objects.all_exclude_flagged().count(), self.increment)

    @patch.object(settings, 'COMMENT_FLAGS_ALLOWED', 0)
    def test_filtering_comment_when_flag_not_enabled(self):
        comment = self.parent_comment_1
        self.assertEqual(Comment.objects.all_exclude_flagged().count(), self.increment)
        self.create_flag_instance(self.user_1, comment)
        self.create_flag_instance(self.user_2, comment)

        comment.flag.get().refresh_from_db()
        self.assertEqual(comment.flag.get().flag_count, 2)

        self.assertEqual(Comment.objects.all_exclude_flagged().count(), self.increment)


    @patch.object(settings, 'COMMENT_FLAGS_ALLOWED', 1)
    @patch.object(settings, 'COMMENT_SHOW_FLAGGED', False)
    def test_all_comments_by_objects(self):

        init_count = self.post_1.comments.count()
        self.assertEqual(init_count, 6)

        comment = self.post_1.comments.first()
        self.create_flag_instance(self.user_1, comment)
        self.create_flag_instance(self.user_2, comment)
        count = Comment.objects.all_comments_by_object(self.post_1).count()
        self.assertEqual(count, init_count - 1)

        count = Comment.objects.all_comments_by_object(self.post_1, include_flagged=True).count()

        self.assertEqual(count, init_count)

    @patch.object(settings, 'COMMENT_FLAGS_ALLOWED', 1)
    @patch.object(settings, 'COMMENT_SHOW_FLAGGED', False)
    def test_get_parent_comment(self):
        self.assertIsNone(Comment.objects.get_parent_comment(''))
        self.assertIsNone(Comment.objects.get_parent_comment('0'))
        self.assertIsNone(Comment.objects.get_parent_comment(100))
        parent_comment = Comment.objects.get_parent_comment(self.parent_comment_1.id)
        self.assertIsNotNone(parent_comment)
        self.assertEqual(parent_comment, self.parent_comment_1)
