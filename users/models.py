import uuid

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone

from users.manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
  """
   User Model

   This replaced the default username field with an email address and I also removed is_staff and is_superuser.
   These fields are fine to have if you have a use for them. In this example, we don’t have any.
  """
  ADMIN = 1
  SELLER = 2
  CASHIER = 3
  ACCOUNTANT = 4

  ROLE_CHOICES = (
    (ADMIN, 'Admin'),
    (SELLER, 'Seller manager'),
    (CASHIER, 'Cashier'),
    (ACCOUNTANT, 'Accountant')
  )

  uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
  email = models.EmailField(unique=True)
  first_name = models.CharField(max_length=30, blank=True)
  last_name = models.CharField(max_length=50, blank=True)
  # default role SELLER
  role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=2)
  date_joined = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=True)
  is_deleted = models.BooleanField(default=False)
  created_date = models.DateTimeField(default=timezone.now)
  modified_date = models.DateTimeField(default=timezone.now)
  created_by = models.EmailField()
  modified_by = models.EmailField()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  objects = CustomUserManager()

  # check if admin
  @property
  def is_admin(self):
    return self.role == 1

  # check if staff
  @property
  def is_staff(self):
    return self.role == 1

  def __str__(self):
    return self.email

  def get_full_name(self):
    return self.first_name + ' ' + self.last_name

  class Meta:
    verbose_name = 'user'
    verbose_name_plural = 'users'
