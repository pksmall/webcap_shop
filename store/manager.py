from datetime import datetime
from django.db import models
from django.utils.timezone import make_aware


class OrderManager(models.Manager):
  def set_paid_status(self, instance):
    if instance.status == self.model.CREATED or instance.status == self.model.PROCESSING:
      instance.status = self.model.PAID
      instance.save()
      return True
    else:
      return False

  def set_processing_status(self, instance):
    if instance.status == self.model.CREATED:
      instance.status = self.model.PROCESSING
      instance.save()
      return True
    else:
      return False

  def set_done_status(self, instance):
    if instance.status == self.model.PAID:
      instance.status = self.model.DONE
      instance.save()
      return True
    else:
      return False

  def get_all(self):
    return super(OrderManager, self).get_queryset().all()

  def get_by_date(self, args):
    try:
      datefrom = make_aware(datetime.strptime(args[0], "%Y%m%d"))
      dateuntil = make_aware(datetime.strptime(args[1], "%Y%m%d"))
    except Exception as ex:
      datefrom = make_aware(datetime.strptime(args[0], "%d.%m.%Y"))
      dateuntil = make_aware(datetime.strptime(args[1], "%d.%m.%Y"))
    print(datefrom, dateuntil)
    return super(OrderManager, self).get_queryset().filter(created__gte=datefrom, created__lte=dateuntil)

  def create_new(self, product, user):
    from .models import Bill

    price = 0.00
    # @todo 30 days and 20% need to move into settings
    """
     check product created_at bigger than 30 days and calculate 20% discount 
     check if discount price more than zero and the real price will be calculated   
     if discount zero than calculate discount and save discount price 
    """
    now_time = datetime.now().replace(tzinfo=None)
    time_between_creation = now_time - product.created_at.replace(tzinfo=None)
    if time_between_creation.days > 30:
      if product.discount_price == 0.00:
        product.discount_price = product.regular_price * 20/100
        product.save()
      price = product.regular_price - product.discount_price
    else:
      price = product.regular_price

    order_key = now_time.strftime("%Y%m%d%H%I%S") + "-" + str(product.pk)
    order = self.model(order_key=order_key, total_paid=price, created_by=user)
    order.save()
    bill = Bill(order=order, product=product, price=price)
    bill.save()
    return order, bill


class ProductManager(models.Manager):
  """
  Product Manager
  """

  def get_all(self):
    return super(ProductManager, self).get_queryset().all()

  def get_queryset(self):
    return super(ProductManager, self).get_queryset().filter(is_active=True)

  def create(self, title, regular_price, who_created, **extra_fields):
    product = self.model(title=title, regular_price=regular_price, who_created=who_created, **extra_fields)
    product.save()
    return product

  def update(self, instance, data):
    # @todo not implemented yet
    pass

  def delete_product(self, data):
    # @todo not implemented yet
    pass
