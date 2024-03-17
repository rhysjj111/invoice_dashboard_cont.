from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Part, Labour

#parts signals
@receiver(post_save, sender=Part)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.invoice.update_total()

@receiver(post_delete, sender=Part)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.invoice.update_total()

#labour signals
@receiver(post_save, sender=Labour)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.invoice.update_total()

@receiver(post_delete, sender=Labour)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.invoice.update_total()