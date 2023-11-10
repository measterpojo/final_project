from django.dispatch import receiver
from django.db.models import signals

from reactions.models import Reaction

from .models import Article
from django.conf import settings


@receiver(signals.post_save, sender=Article)
def add_initial_instances(sender, instance, created, raw, using, update_fields, **kwargs):
    print('asssssssssss')
    if created:
        print('yooo')
        instance.reaction.create()
        instance.flag.create()

