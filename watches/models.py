from django.db import models

# Create your models here.

class Product(models.Model):
  
  id = models.CharField(max_length=255, primary_key=True)
  name = models.CharField(max_length=255)
  thumbnail_url = models.URLField(max_length=255)
  short_description = models.TextField()
  price = models.FloatField()
  list_price = models.FloatField()
  price_usd = models.FloatField()
  discount = models.FloatField()
  discount_rate = models.FloatField()
  rating_average = models.FloatField()
  product_group_name = models.CharField(max_length=255)
  description = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ('name',)
  
  def __str__(self):
    return self.name


class Watch(models.Model):
  ACTIVE = 1
  DELETE = 2
  STATUS_CHOICES = [(ACTIVE, 'Active'), (DELETE, 'Delete')]
  product_id = models.ForeignKey(
    Product,
    related_name='watches',
    on_delete=models.CASCADE,
    null=True,
  )
  expected_price = models.FloatField()
  status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=ACTIVE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ('-updated_at',)

  def __str__(self):
    return self.name