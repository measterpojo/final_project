from typing import Any, Dict, Iterable, Optional, Tuple
from django.db import models

from django.urls import reverse

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.utils import timezone
from .managers import CommentManager

from reactions.models import Reaction
from flags.models import Flag

from django.contrib.contenttypes.fields import GenericRelation

User = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    content = models.TextField()
    urlhash = models.CharField(
        max_length=50,
        unique=True,
        editable=False
        )
    posted = models.DateTimeField(default=timezone.now, editable=False)
    edited = models.DateTimeField(auto_now=True)

    reaction = GenericRelation(Reaction)
    flag = GenericRelation(Flag)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    

    objects = CommentManager()

    class Meta:
        ordering = ['-posted']

    def get_absolute_url(self):
        return reverse('blog:detailbyid', kwargs={
            'article_id': self.content_object.id,
            'year': self.content_object.created_time.year,
            'month': self.content_object.created_time.month,
            'day': self.content_object.created_time.day
        })

    def __str__(self) -> str:
        username = self.user
        _content = self.content[:20]
        if not self.parent:
            return f'comment by {username}: {_content}'
        else:
            return f'reply by {username}: {_content}'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def _set_unique_urlhash(self):
        if not self.urlhash:
            self.urlhash = self.__class__.objects.generate_urlhash()

    # def _set_email(self):
    #     if self.user:
    #         self.email = getattr(self.user, self.user.EMAIL_FIELD, '')

    def save(self, *args, **kwargs):
        self._set_unique_urlhash()
        # self._set_email()
        super(Comment, self).save(*args, **kwargs)


    def replies(self, include_flagged=False):
        manager = self.__class__.objects
        if include_flagged:
            qs = manager.all()
        else:
            qs = manager.all_exclude_flagged()
        return manager._filter_parents(qs, parent=self)
    

    @property
    def is_parent(self):
        return self.parent is None
    


    def _get_reaction_count(self, reaction_type):
        return getattr(self.reaction.get(), reaction_type, None)


    @property
    def likes(self):
        return self._get_reaction_count('likes')

    @property
    def dislikes(self):
        return self._get_reaction_count('dislikes')


    @property
    def is_edited(self):
        if self.user:
            return self.posted.timestamp() + 1 < self.edited.timestamp()
        return False
    
    @property
    def is_flagged(self):
        if hasattr(self, 'flag') and self.flag.get().is_flag_enabled:
            print(self.flag.get().state)
 
            return self.flag.get().state != self.flag.get().UNFLAGGED
        return False
    
    @property
    def has_flagged_state(self):
        if hasattr(self, 'flag'):
            return self.flag.get().state == self.flag.get().FLAGGED
        return False


    @property
    def has_rejected_state(self):
        if hasattr(self, 'flag'):
            return self.flag.get().state == self.flag.get().REJECTED
        return False


    @property
    def has_resolved_state(self):
        if hasattr(self, 'flag'):
            return self.flag.get().state == self.flag.get().RESOLVED
        return False