from django.dispatch import receiver
from django.db.models import signals

from .models import ReactionInstance


@receiver(signals.post_save, sender=ReactionInstance)
def add_count(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        instance.reaction.increase_reaction_count(instance.reaction_type)


@receiver(signals.post_delete, sender=ReactionInstance)
def delete_reaction_instnace(sender, instance, using, **kwargs):
    instance.reaction.decrease_reaction_count(instance.reaction_type)