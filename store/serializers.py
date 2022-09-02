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


class BillCreateSerializer(serializers.ModelSerializer):
  product = serializers.SerializerMethodField()
  is_discount = serializers.SerializerMethodField()
  discount_price = serializers.SerializerMethodField()

  class Meta:
    model = Bill
    fields = ['order', 'product', 'price', 'quantity', 'is_discount', 'discount_price', 'created']

  def get_product(self, instance):
    return instance.product.title

  def get_is_discount(self, instance):
    return instance.product.discount_price > 0.00

  def get_discount_price(self, instance):
    return instance.product.discount_price


class OrderCreateSerializer(serializers.ModelSerializer):
  """
  Order Create Serializer
  """
  class Meta:
    model = Order
    fields = [
      'id',
      'order_key',
      'total_paid',
      'created_by',
      'status',
      'created'
    ]


class OrderPaidSerializer(serializers.ModelSerializer):
  bill = serializers.SerializerMethodField()
  status = serializers.SerializerMethodField()

  class Meta:
    model = Order
    fields = [
      'id',
      'order_key',
      'total_paid',
      'created_by',
      'status',
      'created',
      'bill'
    ]

  def get_status(self, instance):
    res = ""
    for idx, val in Order.STATUS_CHOICES:
      if idx == instance.status:
        res = val
        break
    return res

  def get_bill(self, instance):
    return BillCreateSerializer(Bill.objects.filter(order=instance.pk).get()).data


class OrderListSerializer(serializers.ModelSerializer):
  """
  Order List Serializer
  """
  bill = serializers.SerializerMethodField()
  status = serializers.SerializerMethodField()

  class Meta:
    model = Order
    fields = [
      'id',
      'order_key',
      'total_paid',
      'created_by',
      'status',
      'created',
      'bill'
    ]

  def get_bill(self, instance):
    return BillCreateSerializer(Bill.objects.filter(order=instance.pk).get()).data

  def get_status(self, instance):
    res = ""
    for idx, val in Order.STATUS_CHOICES:
      if idx == instance.status:
        res = val
        break
    return res


class OrderGetSerializer(serializers.ModelSerializer):
  """
  Order Get by Id Serializer
  """
  bill = serializers.SerializerMethodField()
  status = serializers.SerializerMethodField()

  class Meta:
    model = Order
    fields = [
      'id',
      'order_key',
      'total_paid',
      'created_by',
      'status',
      'created',
      'bill'
    ]

  def get_bill(self, instance):
    return BillCreateSerializer(Bill.objects.filter(order=instance.pk).get()).data

  def get_status(self, instance):
    res = ""
    for idx, val in Order.STATUS_CHOICES:
      if idx == instance.status:
        res = val
        break
    return res
