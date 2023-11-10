from django.dispatch import receiver
from django.db.models import signals

from .models import Comment
from django.conf import settings


@receiver(signals.post_save, sender=Comment)
def add_initial_instances(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        instance.reaction.create()
        instance.flag.create()

