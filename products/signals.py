from watches.models import Watch
from django.db.models import F
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Watch)
def increase_watch_count(sender, instance, update_fields=None, **kwargs):
    product = instance.product
    try:
        old_instance = Watch.objects.get(id=instance.id)
    except Watch.DoesNotExist:
        if instance.status == 1:
            product.watch_count = F('watch_count') + 1
            product.save()

    if old_instance.status != instance.status:
        if instance.status == 1:
            product.watch_count = F('watch_count') + 1
        product.watch_count = F('watch_count') - 1

        product.save()


@receiver(pre_delete, sender=Watch)
def decrease_watch_count(sender, instance, **kwargs):
    product = instance.product
    product.watch_count = F('watch_count') - 1
    product.save()
