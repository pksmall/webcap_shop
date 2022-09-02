from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from store.manager import ProductManager, OrderManager
from webcap_shop import settings
from users.models import User


class Product(models.Model):
  """
  Product model
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
  created_at = models.DateTimeField(_("Created at"), default=timezone.now)
  updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
  who_created = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE, related_name="user_product_created")

  REQUIRED_FIELDS = []

  products = ProductManager()

  class Meta:
    ordering = ("-created_at",)
    verbose_name = _("Product")
    verbose_name_plural = _("Products")

  def __str__(self):
    return self.title


class Order(models.Model):
  """
  Orders model
  """
  CREATED = 1
  PROCESSING = 2
  PAID = 3
  DONE = 4

  STATUS_CHOICES = (
    (CREATED, _('Created')),
    (PROCESSING, _('Processing')),
    (PAID, _('Paid')),
    (DONE, _('Done')),
  )

  order_key = models.CharField(max_length=200, blank=True)
  status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, blank=True, null=True, default=CREATED)
  created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_by")
  total_paid = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0.00)
  created = models.DateTimeField(_("Created at"), default=timezone.now)
  updated = models.DateTimeField(_("Updated at"), auto_now=True)

  orders = OrderManager()

  class Meta:
    ordering = ("-created", )

  def __str__(self):
    return str(self.order_key)


class Bill(models.Model):
  """
  Bills model
  """
  order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
  product = models.ForeignKey(Product, related_name="order_item", on_delete=models.CASCADE)
  price = models.DecimalField(max_digits=5, decimal_places=2)
  quantity = models.PositiveIntegerField(default=1)
  created = models.DateTimeField(_("Created at"), auto_now_add=True)

  def __str__(self):
    return str(self.id)
