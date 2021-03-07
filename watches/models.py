from django.db import models
from users.models import CustomUser
# Create your models here.

class Seller(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=255)
  link = models.CharField(max_length=255)
  logo = models.CharField(max_length=255)

  def __str__(self): 
    return self.name


class Product(models.Model):
  id = models.CharField(max_length=255, primary_key=True)
  seller = models.ForeignKey(
    Seller,
    related_name='products',
    on_delete=models.CASCADE,
    null=True,
  )
  name = models.CharField(max_length=255)
  thumbnail_url = models.URLField(max_length=255)
  short_description = models.TextField()
  price = models.FloatField()
  list_price = models.FloatField()
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
  product = models.ForeignKey(
    Product,
    related_name='watches',
    on_delete=models.CASCADE,
    null=True,
  )
  owner = models.ForeignKey(
    CustomUser,
    related_name='watches',
    on_delete=models.CASCADE,
  )
  expected_price = models.FloatField()
  status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=ACTIVE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ('-updated_at',)

  def __str__(self):
    return self.name