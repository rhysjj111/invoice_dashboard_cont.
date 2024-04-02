from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Part, Labour

#parts signals
@receiver(post_save, sender=Part)
def update_on_parts_save(sender, instance, created, **kwargs):
    """
    Update invoice totals upon part add/edit
    """
    instance.invoice.update_total()


@receiver(post_delete, sender=Part)
def update_on_parts_delete(sender, instance, **kwargs):
    """
    Update invoice totals upon part delete
    """
    instance.invoice.update_total()

#labour signals
@receiver(post_save, sender=Labour)
def update_on_labour_save(sender, instance, created, **kwargs):
    """
    Update invoice totals upon labour add/edit
    """
    instance.invoice.update_total()

@receiver(post_delete, sender=Labour)
def update_on_labour_delete(sender, instance, **kwargs):
    """
    Update invoice totals upon labour delete
    """
    instance.invoice.update_total()