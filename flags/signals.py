from django.dispatch import receiver
from django.db.models import signals


from .models import FlagInstance



@receiver(signals.post_save, sender=FlagInstance)
def increase_count(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        instance.flag.increase_count()
        instance.flag.toggle_flagged_state()
    

@receiver(signals.post_delete, sender=FlagInstance)
def decrease_count(sender, instance, using, **kwargs):
    """Decrease flag count in the flag model before deleting an instance"""
    instance.flag.decrease_count()
    instance.flag.toggle_flagged_state()