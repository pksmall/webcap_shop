from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from store.manager import ProductManager
from webcap_shop import settings
from users.models import User


class Product(models.Model):
  """
  The Product model
  """

  title = models.CharField(verbose_name=_("title"), help_text=_("Required"),  max_length=255)
  description = models.TextField(verbose_name=_("description"), help_text=_("Not Required"), blank=True)
  slug = models.SlugField(max_length=255, blank=True)
  regular_price = models.DecimalField(
    verbose_name=_("Regular price"),
    help_text=_("Maximum 999.99"),
    error_messages={
      "name": {
        "max_length": _("The price must be between 0 and 999.99."),
      },
    },
    max_digits=5,
    decimal_places=2,
  )
  discount_price = models.DecimalField(
    verbose_name=_("Discount price"),
    help_text=_("Maximum 999.99"),
    error_messages={
      "name": {
        "max_length": _("The price must be between 0 and 999.99."),
      },
    },
    max_digits=5,
    decimal_places=2,
    default=0.00
  )
  is_active = models.BooleanField(
    verbose_name=_("Product visibility"),
    help_text=_("Change product visibility"),
    default=True,
  )
  created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
  updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
  who_created = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE, related_name="user_product_created")

  REQUIRED_FIELDS = []

  objects = ProductManager()

  class Meta:
    ordering = ("-created_at",)
    verbose_name = _("Product")
    verbose_name_plural = _("Products")

  def __str__(self):
    return self.title
