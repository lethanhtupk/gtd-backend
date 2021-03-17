from users.models import CustomUser, UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff and instance.is_superuser:
            UserProfile.objects.create(user=instance, role=3)
        else:
            if instance.is_seller:
                UserProfile.objects.create(user=instance, role=2)
            else:
                UserProfile.objects.create(user=instance, role=1)
