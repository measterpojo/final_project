from django.core.exceptions import ValidationError
from django.db import IntegrityError

from reactions.models import ReactionInstance
from comments.tests.base import BaseCommentManagerTest, BaseCommentTest


class ReactionInstanceModelTest(BaseCommentManagerTest):
    
    def setUp(self):
        super().setUp()
        self.user = self.user_1
        self.comment = self.child_comment_1
        self.LIKE = ReactionInstance.ReactionType.LIKE.name
        self.DISLIKE = ReactionInstance.ReactionType.DISLIKE.name

    def test_user_can_create_reaction(self):
        """Test whether reaction instance can be created"""
        instance = self.create_reaction_instance(self.user, self.comment, self.LIKE)
        self.assertIsNotNone(instance)