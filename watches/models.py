from django.db import models
from users.models import CustomUser
from products.models import (
    Product
)


class Watch(models.Model):
    ACTIVE = 1
    DEACTIVATE = 2
    DELETE = 3
    STATUS_CHOICES = [(ACTIVE, 'Active'), (DEACTIVATE,
                                           'Deactivate'), (DELETE, 'Delete')]
    product = models.ForeignKey(
        Product,
        related_name='watches',
        on_delete=models.CASCADE,
    )
    owner = models.ForeignKey(
        CustomUser,
        related_name='watches',
        on_delete=models.CASCADE,
    )
    expected_price = models.FloatField()
    lowest_price = models.FloatField()
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated_at',)
