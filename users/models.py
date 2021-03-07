from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from users.managers import CustomUserManager


# Create your models here.

class CustomUser(AbstractUser):
  username = None
  email = models.EmailField(_('email address'), unique=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  objects = CustomUserManager()


class UserProfile(models.Model):
  CUSTOMER = 1
  SELLER = 2 
  ADMIN = 3 
  ROLE_CHOICES = (
    (CUSTOMER, 'Customer'),
    (SELLER, 'Seller'),
    (ADMIN, 'Admin')
  )
  fullname = models.CharField(max_length=255, null=True)
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
  photo_url = models.CharField(max_length=255, null=True)
  role = models.PositiveSmallIntegerField(ROLE_CHOICES, default=1)

  def __str__(self):
    return self.user.email

