from django.db import models


class Seller(models.Model):
    id = models.IntegerField(primary_key=True)
    sku = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    link = models.CharField(max_length=255)
    is_best_store = models.BooleanField()
    logo = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    is_leaf = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    seller = models.ForeignKey(
        Seller,
        related_name='products',
        on_delete=models.CASCADE,
        null=True,
    )
    brand = models.ForeignKey(
        Brand,
        related_name='products',
        on_delete=models.CASCADE,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        null=True
    )
    watch_count = models.PositiveIntegerField(default=0)
    url_path = models.CharField(max_length=255)
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


class Image(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.CASCADE,
    )
    label = models.CharField(max_length=255, null=True)
    position = models.CharField(max_length=255, null=True)
    base_url = models.CharField(max_length=255)
    thumbnail_url = models.CharField(max_length=255)
    small_url = models.CharField(max_length=255)
    medium_url = models.CharField(max_length=255)
    large_url = models.CharField(max_length=255)
    is_gallery = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
