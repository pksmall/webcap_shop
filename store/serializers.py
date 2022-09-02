from datetime import datetime
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import Product, Order, Bill


class ProductCreateSerializer(serializers.ModelSerializer):
  """
  Product Create Serializer
  """
  class Meta:
    model = Product
    fields = [
      'title',
      'regular_price',
      'discount_price',
      'slug',
      'description',
      'is_active',
      'who_created'
    ]

  def create(self, validated_data):
    product = Product.products.create(**validated_data)
    return product

  def validate(self, data):
    if not data['title']:
        raise serializers.ValidationError(_("title required"))
    if not data['regular_price']:
        raise serializers.ValidationError(_("regular_price required"))
    return data


class ProductGetSerializer(serializers.ModelSerializer):
  """
  Product Getter Serializer
  """
  class Meta:
    model = Product
    fields = [
      'id',
      'title',
      'regular_price',
      'discount_price',
      'is_active',
      'created_at',
      'updated_at'
    ]


class OrderCreateSerializer(serializers.ModelSerializer):
  """
  Order Create Serializer
  """
  class Meta:
    model = Order

  def create(self, validated_data):
    product = Product.objects.filter(pk=validated_data['product_id']).get()
    # @todo 30 days and 20% need to move into settings
    """
     check product created_at bigger than 30 days and calculate 20% discount 
     check if discount price more than zero and the real price will be calculated   
     if discount zero than calculate discount and save discount price 
    """
    price = 0.00
    if product.created_at > 30:
      if product.discount_price == 0.00:
        product.discount_price = product.regular_price * 20/100
        product.save()
      price = product.regular_price - product.discount_price
    order_key = datetime.strftime("%Y%m%d%H%I") + "-" + product.pk
    order = Order.objects.create(order_key=order_key, total_paid=price)
    Bill.objects.create(order=order, product=product, quantity=1)
    return order

  def validate(self, data):
    if not data['product_id']:
      try:
        # check if product exists and active
        Product.products.filter(pk=data['product_id']).get()
      except Exception:
        raise serializers.ValidationError(_("product not exists"))
    return data


class OrderListSerializer(serializers.ModelSerializer):
  """
  Order List Serializer
  """
  class Meta:
    model = Order


class OrderUpdateSerializer(serializers.ModelSerializer):
  """
  Order Update Serializer
  """
  class Meta:
    model = Order


class OrderCloseSerializer(serializers.ModelSerializer):
  """
  Order Close Serializer
  """
  class Meta:
    model = Order


class OrderGetSerializer(serializers.ModelSerializer):
  """
  Order Get by Id Serializer
  """
  class Meta:
    model = Order
