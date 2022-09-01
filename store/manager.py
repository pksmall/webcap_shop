from django.db import models


class ProductManager(models.Manager):
  """
  Product Manager
  """

  def get_queryset(self):
    return super(ProductManager, self).get_queryset().filter(is_active=True)

  def create(self,  title, regular_price, who_created, **extra_fields):
    product = self.model(title=title, regular_price=regular_price, who_created=who_created, **extra_fields)
    product.save()
    return product

  def update(self, instance, data):
    # @todo not implemented yet
    pass

  def delete_product(self, data):
    # @todo not implemented yet
    pass
