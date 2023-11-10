from django.db import models

from django.core.exceptions import ValidationError
from django.utils import timezone

from django.conf import settings
from django.contrib.auth import get_user_model

from core.messages import FlagState, FlagError

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .managers import FlagManager, FlagInstanceManager

User = get_user_model()



class Flag(models.Model):

    UNFLAGGED = 1
    FLAGGED = 2
    REJECTED = 3
    RESOLVED = 4

    STATES_CHOICES = [
        (UNFLAGGED, FlagState.UNFLAGGED),
        (FLAGGED, FlagState.FLAGGED),
        (REJECTED, FlagState.REJECTED),
        (RESOLVED, FlagState.RESOLVED),
    ]

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    flag_count = models.PositiveIntegerField(default=0)
    state = models.SmallIntegerField(choices=STATES_CHOICES, default=UNFLAGGED)
    moderator = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank=True,
        related_name='flags_moderated')    

    objects = FlagManager()

    def increase_count(self):
        self.refresh_from_db()
        field = 'flag_count'
        self.flag_count = models.F(field) + 1
        self.save(update_fields=[field])

    
    def decrease_count(self):
        self.refresh_from_db()
        field = 'flag_count'
        self.flag_count = models.F(field) - 1
        self.save(update_fields=[field])

    def get_clean_state(self, state):
        err = ValidationError(FlagError.STATE_INVALID.format(state=state), code='invalid')
        try:
            state = int(state)
            if state not in [st[0] for st in self.STATES_CHOICES]:
                raise err
        except (ValueError, TypeError):
            raise err
        return state

    def toggle_state(self, state, moderator):
        state = self.get_clean_state(state)
        if state != self.REJECTED and state != self.RESOLVED:
            raise ValidationError(FlagError.STATE_INVALID.format(state=state), code='invalid')
        if self.state == state:
            self.state = self.FLAGGED
        else:
            self.state = state
        self.moderator = moderator
        self.save()
    
    def toggle_flagged_state(self):
        allowed_flags = settings.COMMENT_FLAGS_ALLOWED
        if not allowed_flags:
            return 
        self.refresh_from_db()
        if self.flag_count > allowed_flags and self.state not in [self.RESOLVED, self.REJECTED]:
            self.state = self.FLAGGED
            self.save()
        else:
            self.state = self.UNFLAGGED
            self.save()

    @property
    def is_flag_enabled(self):
        return bool(getattr(settings, 'COMMENT_FLAGS_ALLOWED', 0))
    
    @property
    def comment_author(self):
        return self.content_object.user
    
    def get_verbose_state(self, state):
        state = self.get_clean_state(state)
        for item in self.STATES_CHOICES:
            if item[0] == state:
                return item[1]
        return None



class FlagInstance(models.Model):
    flag = models.ForeignKey(Flag, on_delete=models.CASCADE, related_name='flags')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flags')
    info = models.TextField(null=True, blank=True)
    date_flagged = models.DateTimeField(auto_now=timezone.now())

    objects = FlagInstanceManager()
    reason = models.SmallIntegerField(choices=objects.REASONS, default=objects.reason_values[0])

    class Meta:
        unique_together = ('flag', 'user')
        ordering = ('date_flagged',)